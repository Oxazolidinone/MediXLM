from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities import Conversation, Message


class IConversationRepository(ABC):
    @abstractmethod
    async def create(self, conversation: Conversation) -> Conversation:
        pass

    @abstractmethod
    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Conversation]:
        pass

    @abstractmethod
    async def update(self, conversation: Conversation) -> Conversation:
        pass

    @abstractmethod
    async def delete(self, conversation_id: UUID) -> bool:
        pass

    @abstractmethod
    async def add_message(self, message: Message) -> Message:
        pass

    @abstractmethod
    async def get_messages(self, conversation_id: UUID, skip: int = 0, limit: int = 100) -> List[Message]:
        pass
