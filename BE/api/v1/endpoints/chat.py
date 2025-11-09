"""Chat endpoints."""
from typing import Optional, List, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from application.dto import ChatRequestDTO, ChatResponseDTO, MessageDTO
from application.use_cases import ChatUseCase
from api.dependencies import get_chat_use_case
from core.config import settings

router = APIRouter()


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None
    user_id: UUID


class ChatResponse(BaseModel):
    message: str
    conversation_id: UUID
    message_id: UUID
    related_knowledge: Optional[list] = None
    tokens_used: Optional[int] = None
    confidence_score: Optional[float] = None


class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: str
    tokens_used: Optional[int] = None


@router.post("/test-simple", response_model=ChatResponse)
async def test_simple(
    request: ChatRequest,
):
    """Test endpoint without database."""
    return ChatResponse(
        message="Test response - no database access",
        conversation_id=request.user_id,  # Reuse user_id as placeholder
        message_id=request.user_id,
        related_knowledge=[],
        tokens_used=None,
        confidence_score=None,
    )


@router.post("/", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
):
    """Send a message and get AI response."""
    try:
        # Create ChatUseCase directly without dependency injection to avoid greenlet context issues
        from infrastructure.database.connection import get_sync_session
        from infrastructure.repositories.sync_conversation_repository import SyncConversationRepository
        from infrastructure.services import LocalLLMService

        # Run chat in thread
        import asyncio

        def sync_chat_handler():
            """Synchronous chat handler in thread."""
            print("[SYNC] 1. Creating sync session")
            session = get_sync_session()
            print("[SYNC] 2. Session created")
            try:
                print("[SYNC] 3. Creating SyncConversationRepository")
                sync_conv_repo = SyncConversationRepository(session)
                print("[SYNC] 4. Repository created")

                # Get or create conversation
                print("[SYNC] 5. Getting or creating conversation")
                if request.conversation_id:
                    conversation = sync_conv_repo.get_by_id(request.conversation_id)
                    if not conversation:
                        raise ValueError(f"Conversation {request.conversation_id} not found")
                else:
                    from domain.entities import Conversation
                    conversation = Conversation.create(user_id=request.user_id)
                    conversation = sync_conv_repo.create(conversation)

                conversation_id = conversation.id

                # Save user message
                from domain.entities import Message, MessageRole
                user_message = Message.create(
                    conversation_id=conversation_id,
                    role=MessageRole.USER,
                    content=request.message,
                )
                sync_conv_repo.add_message(user_message)
                user_message_id = user_message.id

                # Get conversation history
                messages = sync_conv_repo.get_messages(conversation_id, limit=10)
                conversation_history = [
                    {"role": msg.role.value, "content": msg.content}
                    for msg in messages[:-1]  # Exclude current user message
                ]

                # RAG: Search for relevant knowledge
                print("[SYNC] 6. RAG: Searching for relevant knowledge")
                rag_context = ""
                try:
                    from infrastructure.vector_db.qdrant_client import get_qdrant_client
                    from infrastructure.services.rag_service import RAGService

                    qdrant = get_qdrant_client()
                    rag_service = RAGService(qdrant)
                    rag_result = rag_service.get_context_for_chat(request.message, max_results=3)

                    if rag_result["has_knowledge"]:
                        rag_context = rag_result["context"]
                        print(f"[SYNC] RAG: Found {len(rag_result['knowledge'])} relevant documents")
                    else:
                        print("[SYNC] RAG: No relevant knowledge found")
                except Exception as rag_error:
                    print(f"[SYNC] RAG: Search failed: {rag_error}, continuing without RAG")

                # Generate response with Ollama
                print("[SYNC] 7. Generating response with Ollama")
                try:
                    import ollama
                    from core.config import settings

                    # Build system prompt with RAG context
                    system_prompt = "You are MediXLM, a helpful medical AI assistant. Provide accurate, evidence-based medical information in a clear and concise manner."
                    if rag_context:
                        system_prompt += rag_context

                    response = ollama.chat(
                        model=settings.OLLAMA_MODEL,
                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt
                            },
                            *conversation_history,
                            {"role": "user", "content": request.message}
                        ],
                        options={
                            "temperature": 0.7,
                            "num_predict": 500,  # Max tokens in response
                        }
                    )
                    response_text = response['message']['content']
                    print(f"[SYNC] 8. Ollama response generated: {len(response_text)} chars")

                except Exception as llm_error:
                    print(f"[SYNC] LLM Error: {llm_error}")
                    # Fallback to simple response
                    response_text = "I apologize, but I'm having trouble generating a response right now. Please try again."

                # Save assistant message
                assistant_message = Message.create(
                    conversation_id=conversation_id,
                    role=MessageRole.ASSISTANT,
                    content=response_text,
                )
                sync_conv_repo.add_message(assistant_message)
                assistant_message_id = assistant_message.id

                print("[SYNC] 9. Committing transaction")
                session.commit()
                print("[SYNC] 10. Commit successful")

                return {
                    "message": response_text,
                    "conversation_id": conversation_id,
                    "message_id": assistant_message_id,
                }
            except Exception as e:
                print(f"[SYNC] Exception in sync_chat_handler: {e}")
                import traceback
                traceback.print_exc()
                raise
            finally:
                print("[SYNC] 11. Closing session")
                session.close()
                print("[SYNC] 12. Session closed")

        # Run synchronous chat in thread
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, sync_chat_handler)

        return ChatResponse(
            message=result["message"],
            conversation_id=result["conversation_id"],
            message_id=result["message_id"],
            related_knowledge=[],
            tokens_used=None,
            confidence_score=None,
        )

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Chat error: {error_trace}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/history/{conversation_id}", response_model=list[MessageResponse])
async def get_conversation_history(
    conversation_id: UUID,
    skip: int = 0,
    limit: int = 50,
    chat_use_case: ChatUseCase = Depends(get_chat_use_case),
):
    """Get conversation history."""
    try:
        messages = await chat_use_case.get_conversation_history(
            conversation_id=conversation_id,
            skip=skip,
            limit=limit,
        )

        return [
            MessageResponse(
                id=msg.id,
                conversation_id=msg.conversation_id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at.isoformat(),
                tokens_used=msg.tokens_used,
            )
            for msg in messages
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/test-qdrant")
async def test_qdrant_connection():
    """Test Qdrant connection and check medical knowledge data."""
    try:
        from infrastructure.vector_db.qdrant_client import get_qdrant_client
        from qdrant_client import QdrantClient

        # Get Qdrant client
        qdrant = get_qdrant_client()

        # Get collection info
        collection_info = qdrant.get_collection(settings.QDRANT_COLLECTION_NAME)

        # Sample first 3 points
        points, _ = qdrant.scroll(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            limit=3,
            with_payload=True,
            with_vectors=False
        )

        # Format sample data
        samples = []
        for point in points:
            sample = {
                "id": str(point.id),
                "payload_keys": list(point.payload.keys()),
            }

            # Add text preview if exists
            if 'text' in point.payload:
                text = point.payload['text']
                sample['text_preview'] = text[:200] + "..." if len(text) > 200 else text

            # Add other metadata
            for key in ['source', 'category', 'metadata']:
                if key in point.payload:
                    sample[key] = point.payload[key]

            samples.append(sample)

        return {
            "status": "connected",
            "collection_name": settings.QDRANT_COLLECTION_NAME,
            "total_points": collection_info.points_count,
            "vector_size": collection_info.config.params.vectors.size,
            "distance_metric": str(collection_info.config.params.vectors.distance),
            "sample_data": samples,
            "message": f"✅ Qdrant connected! Found {collection_info.points_count} medical documents."
        }

    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Qdrant test error: {error_trace}")
        return {
            "status": "error",
            "error": str(e),
            "traceback": error_trace,
            "message": "❌ Failed to connect to Qdrant or retrieve data"
        }
