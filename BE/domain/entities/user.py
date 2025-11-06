from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class User:
    id: UUID
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime = None
    updated_at: datetime = None
    is_active: bool = True

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

    @staticmethod
    def create(username: str, email: str, full_name: Optional[str] = None) -> "User":
        return User(
            id=uuid4(),
            username=username,
            email=email,
            full_name=full_name,
        )

    def update_profile(self, full_name: Optional[str] = None, email: Optional[str] = None):
        if full_name:
            self.full_name = full_name
        if email:
            self.email = email
        self.updated_at = datetime.utcnow()

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.utcnow()
