from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class UserCreateDTO:
    username: str
    email: str
    full_name: Optional[str] = None


@dataclass
class UserResponseDTO:
    id: UUID
    username: str
    email: str
    full_name: Optional[str]
    created_at: datetime
    is_active: bool
