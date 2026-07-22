"""Pydantic schemas for authentication requests and responses."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """User registration request body."""

    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    phone_number: str | None = Field(None, max_length=20)


class LoginRequest(BaseModel):
    """User login request body."""

    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    """Token refresh request body."""

    refresh_token: str


class TokenResponse(BaseModel):
    """JWT token pair response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AuthSuccessResponse(BaseModel):
    """Successful authentication response with user and tokens."""

    success: bool = True
    message: str
    data: dict
