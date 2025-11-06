"""Chat use case."""
from typing import Optional, List, Dict, Any
from uuid import UUID

from application.dto import ChatRequestDTO, ChatResponseDTO, MessageDTO
from application.interfaces import ILLMService, IEmbeddingService
from domain.entities import Conversation, Message, MessageRole
from domain.repositories import (
    IConversationRepository,
    IKnowledgeGraphRepository,
    ICacheRepository,
)
from core.exceptions import ConversationNotFoundError, UserNotFoundError
from core.prompts import build_chat_prompt, format_knowledge_context


class ChatUseCase:
    def __init__(
        self,
        conversation_repository: IConversationRepository,
        knowledge_graph_repository: IKnowledgeGraphRepository,
        cache_repository: ICacheRepository,
        llm_service: ILLMService,
        embedding_service: IEmbeddingService,
    ):
        self.conversation_repo = conversation_repository
        self.kg_repo = knowledge_graph_repository
        self.cache_repo = cache_repository
        self.llm_service = llm_service
        self.embedding_service = embedding_service

    async def process_message(self, request: ChatRequestDTO) -> ChatResponseDTO:
        # Get or create conversation
        if request.conversation_id:
            conversation = await self.conversation_repo.get_by_id(request.conversation_id)
            if not conversation:
                raise ConversationNotFoundError(f"Conversation {request.conversation_id} not found")
        else:
            conversation = Conversation.create(user_id=request.user_id)
            conversation = await self.conversation_repo.create(conversation)

        # Save user message
        user_message = Message.create(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.message,
        )
        await self.conversation_repo.add_message(user_message)

        # Generate embeddings for semantic search
        embeddings = await self.embedding_service.generate_embeddings(request.message)

        # Search knowledge graph for relevant medical information
        related_knowledge = await self.kg_repo.similarity_search(
            embeddings=embeddings,
            limit=5
        )

        # Build context from knowledge graph
        knowledge_context = self._build_knowledge_context(related_knowledge)

        # Get conversation history
        messages = await self.conversation_repo.get_messages(conversation.id, limit=10)
        conversation_history = self._build_conversation_history(messages)

        # Generate LLM response
        system_prompt = self._build_system_prompt(knowledge_context)
        llm_response = await self.llm_service.generate_response(
            messages=conversation_history + [{"role": "user", "content": request.message}],
            system_prompt=system_prompt,
            temperature=0.7,
        )

        # Save assistant message
        assistant_message = Message.create(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=llm_response["content"],
            tokens_used=llm_response.get("tokens_used"),
        )
        await self.conversation_repo.add_message(assistant_message)

        # Cache the response
        cache_key = f"chat:{conversation.id}:{user_message.id}"
        await self.cache_repo.set(cache_key, llm_response["content"], expire=3600)

        return ChatResponseDTO(
            message=llm_response["content"],
            conversation_id=conversation.id,
            message_id=assistant_message.id,
            related_knowledge=[
                {
                    "name": k.name,
                    "type": k.knowledge_type.value,
                    "description": k.description,
                }
                for k in related_knowledge
            ],
            tokens_used=llm_response.get("tokens_used"),
            confidence_score=llm_response.get("confidence_score"),
        )

    def _build_knowledge_context(self, knowledge_list) -> str:
        """Build context from knowledge graph."""
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
        """Build conversation history for LLM."""
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages[:-1]  # Exclude the last message (current user message)
        ]

    def _build_system_prompt(self, knowledge_context: str) -> str:
        """Build system prompt with knowledge context."""
        return build_chat_prompt(knowledge_context if knowledge_context else None)

    async def get_conversation_history(
        self, conversation_id: UUID, skip: int = 0, limit: int = 50
    ) -> List[MessageDTO]:
        """Get conversation history."""
        messages = await self.conversation_repo.get_messages(
            conversation_id, skip=skip, limit=limit
        )

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
