from typing import List, Dict
from uuid import UUID

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
        try:
            print("=" * 50)
            print("Step 1: Get or create conversation")
            # Get or create conversation
            try:
                if request.conversation_id:
                    print("  1a: Getting existing conversation")
                    conversation = await self.conversation_repo.get_by_id(request.conversation_id)
                    if not conversation:
                        raise ConversationNotFoundError(f"Conversation {request.conversation_id} not found")
                else:
                    print("  1b: Creating new conversation")
                    conversation = Conversation.create(user_id=request.user_id)
                    print("  1c: Entity created, now saving to DB")
                    conversation = await self.conversation_repo.create(conversation)
                    print("  1d: Conversation saved to DB")
            except Exception as e:
                print(f"  ERROR at step 1: {e}")
                raise

            # Extract primitives from conversation immediately to avoid session binding
            print("Step 2: Extracting conversation ID")
            try:
                conversation_id = conversation.id
                print(f"Step 2 OK: Conversation ID = {conversation_id}")
            except Exception as e:
                print(f"  ERROR extracting ID: {e}")
                raise

            # Save user message
            print("Step 3: Creating user message")
            try:
                user_message = Message.create(
                    conversation_id=conversation_id,
                    role=MessageRole.USER,
                    content=request.message,
                )
                print("  Step 3a: User message entity created")
                await self.conversation_repo.add_message(user_message)
                print("  Step 3b: User message saved to DB")
            except Exception as e:
                print(f"  ERROR at step 3: {e}")
                raise

            # Extract primitives from user message
            print("Step 4: Extracting user message ID")
            try:
                user_message_id = user_message.id
                user_message_content = request.message
                print("Step 4 OK: User message ID extracted")
            except Exception as e:
                print(f"  ERROR at step 4: {e}")
                raise

            # Get conversation history
            print("Step 5: Getting conversation history")
            messages = await self.conversation_repo.get_messages(conversation_id, limit=4)

            # Convert to primitives IMMEDIATELY to detach from session
            conversation_history = []
            for msg in messages[:-1]:
                # Force evaluation of lazy attributes
                conversation_history.append({
                    "role": str(msg.role.value),  # Convert enum to string
                    "content": str(msg.content)     # Ensure it's a string
                })
            print("Step 6: Conversation history ready")

            # Skip embeddings for now
            print("Step 7: Skipping embeddings")
            embeddings = []
            print(f"Step 8: Embeddings skipped")

            # Generate LLM response directly
            print("Step 9: Generating LLM response (SYNC)")
            response_text = "Test response - LLM disabled for debugging"
            print(f"Step 10: LLM response ready")

            # Skip knowledge graph for now
            print("Step 11: Skipping knowledge graph")
            related_knowledge_data = []
            print("Step 13: Knowledge context skipped")

            # Save assistant message
            print("Step 14: Creating assistant message")
            assistant_message = Message.create(
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content=response_text,
            )
            await self.conversation_repo.add_message(assistant_message)
            print("Step 15: Assistant message saved")

            # Cache the response
            cache_key = f"chat:{conversation_id}:{user_message_id}"
            await self.cache_repo.set(cache_key, response_text, expire=3600)
            print("Step 16: Response cached")

            # Extract primitives from assistant message
            assistant_message_id = assistant_message.id

            print("Step 17: Returning response")
            return ChatResponseDTO(
                message=response_text,
                conversation_id=conversation_id,
                message_id=assistant_message_id,
                related_knowledge=related_knowledge_data,
                tokens_used=None,
                confidence_score=None,
            )
        except Exception as e:
            import traceback
            print(f"Error in process_message: {traceback.format_exc()}")
            raise

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

    async def get_conversation_history( self, conversation_id: UUID, skip: int = 0, limit: int = 50) -> List[MessageDTO]:
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
