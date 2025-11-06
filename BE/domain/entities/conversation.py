"""Conversation entity."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from .message import Message


@dataclass
class Conversation:
    """Conversation domain entity."""

    id: UUID
    user_id: UUID
    title: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True
    messages: List[Message] = field(default_factory=list)

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    @staticmethod
    def create(user_id: UUID, title: Optional[str] = None) -> "Conversation":
        """Create a new conversation."""
        return Conversation(
            id=uuid4(),
            user_id=user_id,
            title=title or f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        )

    def add_message(self, message: Message):
        """Add message to conversation."""
        self.messages.append(message)
        self.updated_at = datetime.utcnow()

    def update_title(self, title: str):
        """Update conversation title."""
        self.title = title
        self.updated_at = datetime.utcnow()

    def close(self):
        """Close/deactivate conversation."""
        self.is_active = False
        self.updated_at = datetime.utcnow()
