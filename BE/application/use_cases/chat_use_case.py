from typing import List, Dict
from uuid import UUID

from application.dto import ChatRequestDTO, ChatResponseDTO, MessageDTO
from infrastructure.services.local_llm_service import LocalLLMService  
from domain.entities import Conversation, Message, MessageRole
from domain.repositories import (
    IConversationRepository,
    IKnowledgeGraphRepository,
    ICacheRepository,
)
from core.exceptions import ConversationNotFoundError
from core.prompts import build_chat_prompt, format_knowledge_context


class ChatUseCase:
    def __init__(
        self,
        conversation_repository: IConversationRepository,
        knowledge_graph_repository: IKnowledgeGraphRepository,
        cache_repository: ICacheRepository,
        llm_service: LocalLLMService, 
    ):
        self.conversation_repo = conversation_repository
        self.kg_repo = knowledge_graph_repository
        self.cache_repo = cache_repository
        self.llm_service = llm_service

    async def process_message(self, request: ChatRequestDTO) -> ChatResponseDTO:
        if request.conversation_id:
            conversation = await self.conversation_repo.get_by_id(request.conversation_id)
            if not conversation:
                raise ConversationNotFoundError(f"Conversation {request.conversation_id} not found")
        else:
            conversation = Conversation.create(user_id=request.user_id)
            conversation = await self.conversation_repo.create(conversation)

        user_message = Message.create(
            conversation_id=conversation.id,
            role=MessageRole.USER,
            content=request.message,
        )
        await self.conversation_repo.add_message(user_message)

        query_vecs = await self.llm_service.generate_batch_embeddings([request.message])  # ✅
        query_vec = query_vecs[0]

        try:
            related_knowledge = await self.kg_repo.similarity_search(embedding=query_vec, limit=5)
        except TypeError:
            related_knowledge = await self.kg_repo.similarity_search(embeddings=[query_vec], limit=5)

        # 5) Build context + history
        knowledge_context = self._build_knowledge_context(related_knowledge)
        messages = await self.conversation_repo.get_messages(conversation.id, limit=4)
        conversation_history = self._build_conversation_history(messages)
        system_prompt = self._build_system_prompt(knowledge_context)

        answer_chunks: List[str] = []
        async for chunk in self.llm_service.generate_streaming_response(
            messages=conversation_history + [{"role": "user", "content": request.message}],
            temperature=0.2,
            max_tokens=None,
            system_prompt=system_prompt,
        ):
            answer_chunks.append(chunk)
        answer_text = "".join(answer_chunks).strip() 

        assistant_message = Message.create(
            conversation_id=conversation.id,
            role=MessageRole.ASSISTANT,
            content=answer_text,
            tokens_used=None,  
        )
        await self.conversation_repo.add_message(assistant_message)

        # 8) Cache response
        cache_key = f"chat:{conversation.id}:{user_message.id}"
        await self.cache_repo.set(cache_key, answer_text, expire=3600)

        return ChatResponseDTO(
            message=answer_text,
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
            tokens_used=None,
            confidence_score=None,
        )

    def _build_knowledge_context(self, knowledge_list) -> str:
        knowledge_items = [
            {"name": k.name, "type": k.knowledge_type.value, "description": k.description}
            for k in knowledge_list
        ]
        return format_knowledge_context(knowledge_items)

    def _build_conversation_history(self, messages: List[Message]) -> List[Dict[str, str]]:
        return [{"role": msg.role.value, "content": msg.content} for msg in messages[:-1]]

    def _build_system_prompt(self, knowledge_context: str) -> str:
        return build_chat_prompt(knowledge_context if knowledge_context else None)

    async def get_conversation_history(self, conversation_id: UUID, skip: int = 0, limit: int = 50) -> List[MessageDTO]:
        messages = await self.conversation_repo.get_messages(conversation_id, skip=skip, limit=limit)
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
