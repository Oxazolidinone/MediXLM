"""User endpoints."""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr

from application.dto import UserCreateDTO, UserResponseDTO
from application.use_cases import UserUseCase
from core.exceptions import UserAlreadyExistsError, UserNotFoundError
from presentation.api.dependencies import get_user_use_case

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: UUID
    username: str
    email: str
    full_name: Optional[str]
    created_at: str
    is_active: bool


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_use_case: UserUseCase = Depends(get_user_use_case),
):
    """Create a new user."""
    try:
        dto = UserCreateDTO(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
        )

        response = await user_use_case.create_user(dto)

        return UserResponse(
            id=response.id,
            username=response.username,
            email=response.email,
            full_name=response.full_name,
            created_at=response.created_at.isoformat(),
            is_active=response.is_active,
        )

    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    user_use_case: UserUseCase = Depends(get_user_use_case),
):
    """Get user by ID."""
    try:
        response = await user_use_case.get_user(user_id)

        return UserResponse(
            id=response.id,
            username=response.username,
            email=response.email,
            full_name=response.full_name,
            created_at=response.created_at.isoformat(),
            is_active=response.is_active,
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str,
    user_use_case: UserUseCase = Depends(get_user_use_case),
):
    """Get user by username."""
    try:
        response = await user_use_case.get_user_by_username(username)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found",
            )

        return UserResponse(
            id=response.id,
            username=response.username,
            email=response.email,
            full_name=response.full_name,
            created_at=response.created_at.isoformat(),
            is_active=response.is_active,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
