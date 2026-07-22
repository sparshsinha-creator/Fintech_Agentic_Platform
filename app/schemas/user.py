"""Pydantic schemas for user-related requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """Public user profile response."""

    id: str
    full_name: str
    email: str
    phone_number: str | None
    role: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserUpdateRequest(BaseModel):
    """Update own profile request body."""

    full_name: str | None = Field(None, min_length=1, max_length=255)
    phone_number: str | None = Field(None, max_length=20)


class ChangePasswordRequest(BaseModel):
    """Change password request body."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=128)


class UserListResponse(BaseModel):
    """Paginated user list response."""

    items: list[UserResponse]
    total: int
    page: int
    limit: int


class RoleUpdateRequest(BaseModel):
    """Admin request to change a user's role."""

    role: str = Field(..., pattern=r"^(user|admin)$")


class StandardResponse(BaseModel):
    """Standard API envelope response."""

    success: bool = True
    message: str
    data: dict | None = None
