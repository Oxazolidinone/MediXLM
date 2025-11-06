"""Chat DTOs."""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from uuid import UUID


@dataclass
class ChatRequestDTO:
    message: str
    conversation_id: Optional[UUID] = None
    user_id: UUID = None
    context: Optional[Dict[str, Any]] = None


@dataclass
class ChatResponseDTO:
    message: str
    conversation_id: UUID
    message_id: UUID
    related_knowledge: Optional[List[Dict[str, Any]]] = None
    tokens_used: Optional[int] = None
    confidence_score: Optional[float] = None
