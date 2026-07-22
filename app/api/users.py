"""User management API routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session as SaSession

from app.core.dependencies import get_current_admin, get_current_user
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.user import (
    ChangePasswordRequest,
    RoleUpdateRequest,
    StandardResponse,
    UserUpdateRequest,
)
from app.services.user_service import UserService

router = APIRouter(tags=["Users"])


@router.get("/me")
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
    db: SaSession = Depends(get_db),
) -> StandardResponse:
    """Return the authenticated user's profile."""
    service = UserService(db)
    profile = service.get_profile(current_user.id)
    return StandardResponse(message="Profile retrieved", data=profile)


@router.put("/me")
def update_current_user_profile(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: SaSession = Depends(get_db),
) -> StandardResponse:
    """Update the authenticated user's profile."""
    service = UserService(db)
    profile = service.update_profile(current_user.id, request)
    return StandardResponse(message="Profile updated", data=profile)


@router.put("/me/password")
def change_current_user_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: SaSession = Depends(get_db),
) -> StandardResponse:
    """Change the authenticated user's password."""
    service = UserService(db)
    service.change_password(current_user.id, request)
    return StandardResponse(message="Password changed")


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: SaSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> StandardResponse:
    """List all users (admin only)."""
    service = UserService(db)
    result = service.get_all_users(page=page, limit=limit)
    return StandardResponse(message="Users retrieved", data=result)


@router.get("/users/{user_id}")
def get_user(
    user_id: str,
    db: SaSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> StandardResponse:
    """Get a specific user by ID (admin only)."""
    service = UserService(db)
    profile = service.get_profile(user_id)
    return StandardResponse(message="User retrieved", data=profile)


@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: str,
    request: RoleUpdateRequest,
    db: SaSession = Depends(get_db),
    current_user: User = Depends(get_current_admin),
) -> StandardResponse:
    """Change a user's role (admin only)."""
    service = UserService(db)
    profile = service.update_role(user_id, request.role)
    return StandardResponse(message="Role updated", data=profile)
