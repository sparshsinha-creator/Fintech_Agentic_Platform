"""Authentication service: registration, login, token management."""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.exceptions.handlers import ConflictError, UnauthorizedError
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest

logger = logging.getLogger(__name__)


class AuthService:
    """Business logic for authentication flows."""

    def __init__(self, db: Session) -> None:
        self._repo = UserRepository(db)

    def register(self, request: RegisterRequest) -> dict:
        """Register a new user and return their profile with tokens."""
        existing = self._repo.get_by_email(request.email)
        if existing:
            raise ConflictError(f"Email '{request.email}' is already registered")

        password_hash = hash_password(request.password)
        user = self._repo.create(
            full_name=request.full_name,
            email=request.email,
            password_hash=password_hash,
            phone_number=request.phone_number,
        )

        logger.info("User registered: %s (%s)", user.id, user.email)

        tokens = self._generate_tokens(user)
        return {
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "role": user.role,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat(),
            },
            **tokens,
        }

    def login(self, request: LoginRequest) -> dict:
        """Authenticate a user and return their profile with tokens."""
        user = self._repo.get_by_email(request.email)
        if not user:
            raise UnauthorizedError("Invalid email or password")

        if not verify_password(request.password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")

        if not user.is_active:
            raise UnauthorizedError("Account is deactivated")

        logger.info("User logged in: %s (%s)", user.id, user.email)

        tokens = self._generate_tokens(user)
        return {
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "phone_number": user.phone_number,
                "role": user.role,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "created_at": user.created_at.isoformat(),
            },
            **tokens,
        }

    def refresh_token(self, request: RefreshRequest) -> dict:
        """Issue a new access token from a valid refresh token."""
        try:
            payload = decode_token(request.refresh_token)
        except Exception:
            raise UnauthorizedError("Invalid or expired refresh token")

        if payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid token type")

        user_id = payload.get("sub")
        user = self._repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or deactivated")

        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role,
        )

        return {"access_token": access_token, "token_type": "bearer"}

    def _generate_tokens(self, user) -> dict:
        access_token = create_access_token(
            user_id=user.id,
            email=user.email,
            role=user.role,
        )
        refresh_token = create_refresh_token(
            user_id=user.id,
            email=user.email,
            role=user.role,
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
