"""Chat endpoints."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from application.dto import ChatRequestDTO, ChatResponseDTO, MessageDTO
from application.use_cases import ChatUseCase
from api.dependencies import get_chat_use_case

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
    chat_use_case: ChatUseCase = Depends(get_chat_use_case),
):
    """Send a message and get AI response."""
    try:
        dto_request = ChatRequestDTO(
            message=request.message,
            conversation_id=request.conversation_id,
            user_id=request.user_id,
        )

        response = await chat_use_case.process_message(dto_request)

        return ChatResponse(
            message=response.message,
            conversation_id=response.conversation_id,
            message_id=response.message_id,
            related_knowledge=response.related_knowledge,
            tokens_used=response.tokens_used,
            confidence_score=response.confidence_score,
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
