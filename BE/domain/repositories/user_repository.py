"""User repository interface."""
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities import User


class IUserRepository(ABC):
    """Interface for user repository."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """Create a new user."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID."""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Update user."""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Delete user."""
        pass
