"""Message entity."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any
from uuid import UUID, uuid4


class MessageRole(str, Enum):
    """Message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    """Message domain entity."""

    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    created_at: datetime = None
    metadata: Optional[Dict[str, Any]] = None
    tokens_used: Optional[int] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}

    @staticmethod
    def create(
        conversation_id: UUID,
        role: MessageRole,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        tokens_used: Optional[int] = None
    ) -> "Message":
        """Create a new message."""
        return Message(
            id=uuid4(),
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata=metadata or {},
            tokens_used=tokens_used,
        )

    def add_metadata(self, key: str, value: Any):
        """Add metadata to message."""
        if self.metadata is None:
            self.metadata = {}
        self.metadata[key] = value
