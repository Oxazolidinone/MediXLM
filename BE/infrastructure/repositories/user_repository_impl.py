"""User repository implementation."""
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities import User
from domain.repositories import IUserRepository
from infrastructure.database.models import UserModel


class UserRepositoryImpl(IUserRepository):
    """User repository implementation using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        """Create a new user."""
        user_model = UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
        )
        self.session.add(user_model)
        self.session.flush()
        return self._to_entity(user_model)

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        result = self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        result = self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    def update(self, user: User) -> User:
        """Update user."""
        result = self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one()

        user_model.username = user.username
        user_model.email = user.email
        user_model.full_name = user.full_name
        user_model.updated_at = user.updated_at
        user_model.is_active = user.is_active

        self.session.flush()
        return self._to_entity(user_model)

    def delete(self, user_id: UUID) -> bool:
        """Delete user."""
        result = self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()

        if user_model:
            self.session.delete(user_model)
            self.session.flush()
            return True
        return False

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        """Convert model to entity."""
        return User(
            id=model.id,
            username=model.username,
            email=model.email,
            full_name=model.full_name,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
        )
