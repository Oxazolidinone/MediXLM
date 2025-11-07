from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class MessageDTO(BaseModel):
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
    tokens_used: Optional[int] = None

    class Config:
        from_attributes = True


class ConversationDTO(BaseModel):
    id: UUID
    user_id: UUID
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool
    messages: Optional[List[MessageDTO]] = None

    class Config:
        from_attributes = True
