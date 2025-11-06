"""Conversation repository implementation."""
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from domain.entities import Conversation, Message, MessageRole
from domain.repositories import IConversationRepository
from infrastructure.database.models import ConversationModel, MessageModel


class ConversationRepositoryImpl(IConversationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, conversation: Conversation) -> Conversation:
        """Create a new conversation."""
        conversation_model = ConversationModel(
            id=conversation.id,
            user_id=conversation.user_id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            is_active=conversation.is_active,
        )
        self.session.add(conversation_model)
        await self.session.flush()
        return self._to_entity(conversation_model)

    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get conversation by ID."""
        result = await self.session.execute(
            select(ConversationModel)
            .options(selectinload(ConversationModel.messages))
            .where(ConversationModel.id == conversation_id)
        )
        conversation_model = result.scalar_one_or_none()
        return self._to_entity(conversation_model) if conversation_model else None

    async def get_by_user_id(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Conversation]:
        """Get all conversations for a user."""
        result = await self.session.execute(
            select(ConversationModel)
            .where(ConversationModel.user_id == user_id)
            .order_by(ConversationModel.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        conversation_models = result.scalars().all()
        return [self._to_entity(model) for model in conversation_models]

    async def update(self, conversation: Conversation) -> Conversation:
        """Update conversation."""
        result = await self.session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation.id)
        )
        conversation_model = result.scalar_one()

        conversation_model.title = conversation.title
        conversation_model.updated_at = conversation.updated_at
        conversation_model.is_active = conversation.is_active

        await self.session.flush()
        return self._to_entity(conversation_model)

    async def delete(self, conversation_id: UUID) -> bool:
        """Delete conversation."""
        result = await self.session.execute(
            select(ConversationModel).where(ConversationModel.id == conversation_id)
        )
        conversation_model = result.scalar_one_or_none()

        if conversation_model:
            await self.session.delete(conversation_model)
            await self.session.flush()
            return True
        return False

    async def add_message(self, message: Message) -> Message:
        """Add message to conversation."""
        message_model = MessageModel(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role.value,
            content=message.content,
            created_at=message.created_at,
            metadata=message.metadata,
            tokens_used=message.tokens_used,
        )
        self.session.add(message_model)
        await self.session.flush()
        return self._message_to_entity(message_model)

    async def get_messages(
        self, conversation_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Message]:
        """Get messages for a conversation."""
        result = await self.session.execute(
            select(MessageModel)
            .where(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        message_models = result.scalars().all()
        return [self._message_to_entity(model) for model in message_models]

    @staticmethod
    def _to_entity(model: ConversationModel) -> Conversation:
        """Convert model to entity."""
        conversation = Conversation(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
        )

        if hasattr(model, "messages") and model.messages:
            conversation.messages = [
                ConversationRepositoryImpl._message_to_entity(msg)
                for msg in model.messages
            ]

        return conversation

    @staticmethod
    def _message_to_entity(model: MessageModel) -> Message:
        """Convert message model to entity."""
        return Message(
            id=model.id,
            conversation_id=model.conversation_id,
            role=MessageRole(model.role),
            content=model.content,
            created_at=model.created_at,
            metadata=model.metadata,
            tokens_used=model.tokens_used,
        )
