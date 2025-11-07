from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserCreateDTO(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponseDTO(BaseModel):
    id: UUID
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime
    is_active: bool

    class Config:
        from_attributes = True
