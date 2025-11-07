from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from uuid import UUID


class ChatRequestDTO(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    context: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class ChatResponseDTO(BaseModel):
    message: str
    conversation_id: UUID
    message_id: UUID
    related_knowledge: Optional[List[Dict[str, Any]]] = None
    tokens_used: Optional[int] = None
    confidence_score: Optional[float] = None

    class Config:
        from_attributes = True
