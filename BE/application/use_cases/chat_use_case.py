from typing import List, Dict
from uuid import UUID
import asyncio

from application.dto import ChatRequestDTO, ChatResponseDTO, MessageDTO
from infrastructure.services import LLMService
from domain.entities import Conversation, Message, MessageRole
from domain.repositories import (
    IConversationRepository,
    IKnowledgeGraphRepository,
    ICacheRepository,
)
from core.exceptions import ConversationNotFoundError
from core.prompts import build_chat_prompt, format_knowledge_context


class ChatUseCase:
    def __init__(self, conversation_repository: IConversationRepository, knowledge_graph_repository: IKnowledgeGraphRepository, cache_repository: ICacheRepository, llm_service: LLMService, embedding_service: LLMService):
        self.conversation_repo = conversation_repository
        self.kg_repo = knowledge_graph_repository
        self.cache_repo = cache_repository
        self.llm_service = llm_service
        self.embedding_service = embedding_service

    async def process_message(self, request: ChatRequestDTO) -> ChatResponseDTO:
        """Process message using threaded synchronous database operations."""
        from infrastructure.database.connection import get_sync_session
        from infrastructure.repositories.sync_conversation_repository import SyncConversationRepository
        from infrastructure.cache.redis_client import get_redis_client

        def sync_db_operations():
            """Synchronous database operations in a thread."""
            session = get_sync_session()
            try:
                redis = get_redis_client()
                sync_conv_repo = SyncConversationRepository(session)

                # Get or create conversation
                if request.conversation_id:
                    conversation = sync_conv_repo.get_by_id(request.conversation_id)
                    if not conversation:
                        raise ConversationNotFoundError(f"Conversation {request.conversation_id} not found")
                else:
                    conversation = Conversation.create(user_id=request.user_id)
                    conversation = sync_conv_repo.create(conversation)

                conversation_id = conversation.id

                # Save user message
                user_message = Message.create(
                    conversation_id=conversation_id,
                    role=MessageRole.USER,
                    content=request.message,
                )
                sync_conv_repo.add_message(user_message)
                user_message_id = user_message.id

                # Get conversation history
                messages = sync_conv_repo.get_messages(conversation_id, limit=4)
                conversation_history = [
                    {"role": msg.role.value, "content": msg.content}
                    for msg in messages[:-1]
                ]

                # Generate response
                response_text = "Test response - LLM disabled for debugging"

                # Save assistant message
                assistant_message = Message.create(
                    conversation_id=conversation_id,
                    role=MessageRole.ASSISTANT,
                    content=response_text,
                )
                sync_conv_repo.add_message(assistant_message)
                assistant_message_id = assistant_message.id

                # Skip caching in sync version for now

                session.commit()

                return {
                    "message": response_text,
                    "conversation_id": conversation_id,
                    "message_id": assistant_message_id,
                    "related_knowledge": [],
                }
            finally:
                session.close()

        # Run sync database operations in thread to avoid blocking event loop
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, sync_db_operations)

        return ChatResponseDTO(
            message=result["message"],
            conversation_id=result["conversation_id"],
            message_id=result["message_id"],
            related_knowledge=result["related_knowledge"],
            tokens_used=None,
            confidence_score=None,
        )

    def _build_knowledge_context(self, knowledge_list) -> str:
        knowledge_items = [
            {
                "name": k.name,
                "type": k.knowledge_type.value,
                "description": k.description,
            }
            for k in knowledge_list
        ]
        return format_knowledge_context(knowledge_items)

    def _build_conversation_history(self, messages: List[Message]) -> List[Dict[str, str]]:
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages[:-1] 
        ]

    def _build_system_prompt(self, knowledge_context: str) -> str:
        return build_chat_prompt(knowledge_context if knowledge_context else None)

    async def get_conversation_history(self, conversation_id: UUID, skip: int = 0, limit: int = 50) -> List[MessageDTO]:
        """Get conversation history - wraps sync database call in executor."""
        def sync_get_messages():
            return self.conversation_repo.get_messages(conversation_id, skip=skip, limit=limit)

        loop = asyncio.get_event_loop()
        messages = await loop.run_in_executor(None, sync_get_messages)

        return [
            MessageDTO(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role.value,
                content=msg.content,
                created_at=msg.created_at,
                tokens_used=msg.tokens_used,
            )
            for msg in messages
        ]
