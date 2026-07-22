"""Shared FastAPI dependencies: settings, auth, and RBAC."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session as SaSession

from app.config.settings import Settings, settings as _settings
from app.core.security import decode_token
from app.database.dependencies import get_db
from app.exceptions.handlers import UnauthorizedError
from app.models.user import User
from app.repositories.user_repository import UserRepository

security_scheme = HTTPBearer(auto_error=False)


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return _settings


def get_request_id(request: Request) -> str:
    """Extract or generate a unique request identifier."""
    return request.headers.get("X-Request-ID", "")


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security_scheme),
    db: SaSession = Depends(get_db),
) -> User:
    """Validate the JWT access token and return the authenticated user."""
    if credentials is None:
        raise UnauthorizedError("Authentication required")

    token = credentials.credentials
    try:
        payload = decode_token(token)
    except Exception:
        raise UnauthorizedError("Invalid or expired token")

    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user or not user.is_active:
        raise UnauthorizedError("User not found or deactivated")

    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Ensure the authenticated user has the admin role."""
    if current_user.role != "admin":
        raise UnauthorizedError("Admin privileges required")
    return current_user
