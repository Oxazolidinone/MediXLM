"""User use case."""
import asyncio
from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError
from application.dto import UserCreateDTO, UserResponseDTO
from domain.entities import User
from domain.repositories import IUserRepository
from core.exceptions import UserAlreadyExistsError, UserNotFoundError
from infrastructure.database.connection import get_database_session
from infrastructure.repositories import UserRepositoryImpl


class UserUseCase:
    def __init__(self, user_repository: IUserRepository):
        self.user_repo = user_repository

    async def create_user(self, user_data: UserCreateDTO) -> UserResponseDTO:
        """Create user - uses fresh session in thread executor."""
        def sync_operations():
            try:
                with get_database_session() as session:
                    user_repo = UserRepositoryImpl(session)

                    existing_user = user_repo.get_by_username(user_data.username)
                    if existing_user:
                        raise UserAlreadyExistsError(f"Username {user_data.username} already exists")

                    existing_email = user_repo.get_by_email(user_data.email)
                    if existing_email:
                        raise UserAlreadyExistsError(f"Email {user_data.email} already exists")

                    # Create user entity
                    user = User.create(
                        username=user_data.username,
                        email=user_data.email,
                        full_name=user_data.full_name,
                    )

                    # Save to repository
                    return user_repo.create(user)
            except IntegrityError:
                # Handle database constraint violations (race condition)
                raise UserAlreadyExistsError(
                    f"User with email {user_data.email} or username {user_data.username} already exists"
                )

        loop = asyncio.get_event_loop()
        created_user = await loop.run_in_executor(None, sync_operations)

        return UserResponseDTO(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            full_name=created_user.full_name,
            created_at=created_user.created_at,
            is_active=created_user.is_active,
        )

    async def get_user(self, user_id: UUID) -> UserResponseDTO:
        """Get user by ID - uses fresh session in thread executor."""
        def sync_get():
            with get_database_session() as session:
                user_repo = UserRepositoryImpl(session)
                user = user_repo.get_by_id(user_id)
                if not user:
                    raise UserNotFoundError(f"User {user_id} not found")
                return user

        loop = asyncio.get_event_loop()
        user = await loop.run_in_executor(None, sync_get)

        return UserResponseDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at,
            is_active=user.is_active,
        )

    async def get_user_by_username(self, username: str) -> Optional[UserResponseDTO]:
        """Get user by username - uses fresh session in thread executor."""
        def sync_get():
            with get_database_session() as session:
                user_repo = UserRepositoryImpl(session)
                return user_repo.get_by_username(username)

        loop = asyncio.get_event_loop()
        user = await loop.run_in_executor(None, sync_get)

        if not user:
            return None

        return UserResponseDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at,
            is_active=user.is_active,
        )

    async def update_user_profile(
        self, user_id: UUID, full_name: Optional[str] = None, email: Optional[str] = None
    ) -> UserResponseDTO:
        """Update user profile - uses fresh session in thread executor."""
        def sync_operations():
            with get_database_session() as session:
                user_repo = UserRepositoryImpl(session)
                user = user_repo.get_by_id(user_id)
                if not user:
                    raise UserNotFoundError(f"User {user_id} not found")

                user.update_profile(full_name=full_name, email=email)
                return user_repo.update(user)

        loop = asyncio.get_event_loop()
        updated_user = await loop.run_in_executor(None, sync_operations)

        return UserResponseDTO(
            id=updated_user.id,
            username=updated_user.username,
            email=updated_user.email,
            full_name=updated_user.full_name,
            created_at=updated_user.created_at,
            is_active=updated_user.is_active,
        )
