from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from uuid import UUID


@dataclass
class MessageDTO:
    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
    tokens_used: Optional[int] = None


@dataclass
class ConversationDTO:
    id: UUID
    user_id: UUID
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool
    messages: Optional[List[MessageDTO]] = None
