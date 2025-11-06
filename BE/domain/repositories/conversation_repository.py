"""Conversation repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities import Conversation, Message


class IConversationRepository(ABC):
    """Interface for conversation repository."""

    @abstractmethod
    async def create(self, conversation: Conversation) -> Conversation:
        """Create a new conversation."""
        pass

    @abstractmethod
    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get conversation by ID."""
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Conversation]:
        """Get all conversations for a user."""
        pass

    @abstractmethod
    async def update(self, conversation: Conversation) -> Conversation:
        """Update conversation."""
        pass

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> bool:
        """Delete conversation."""
        pass

    @abstractmethod
    async def add_message(self, message: Message) -> Message:
        """Add message to conversation."""
        pass

    @abstractmethod
    async def get_messages(self, conversation_id: UUID, skip: int = 0, limit: int = 100) -> List[Message]:
        """Get messages for a conversation."""
        pass
