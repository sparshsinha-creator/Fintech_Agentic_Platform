"""Authentication API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SaSession

from app.database.dependencies import get_db
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest
from app.schemas.user import StandardResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=201)
def register(request: RegisterRequest, db: SaSession = Depends(get_db)) -> StandardResponse:
    """Register a new user account."""
    service = AuthService(db)
    result = service.register(request)
    return StandardResponse(message="Registration successful", data=result)


@router.post("/login")
def login(request: LoginRequest, db: SaSession = Depends(get_db)) -> StandardResponse:
    """Authenticate with email and password."""
    service = AuthService(db)
    result = service.login(request)
    return StandardResponse(message="Login successful", data=result)


@router.post("/refresh")
def refresh(request: RefreshRequest, db: SaSession = Depends(get_db)) -> StandardResponse:
    """Issue a new access token using a refresh token."""
    service = AuthService(db)
    result = service.refresh_token(request)
    return StandardResponse(message="Token refreshed", data=result)


@router.post("/logout")
def logout() -> StandardResponse:
    """Logout (client-side token discard).

    In this stateless JWT implementation, logout is handled
    by the client removing the stored tokens.
    """
    return StandardResponse(message="Logged out successfully")
