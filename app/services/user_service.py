"""User profile service: read, update, password change."""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.exceptions.handlers import NotFoundError, UnauthorizedError, ValidationError
from app.repositories.user_repository import UserRepository
from app.schemas.user import ChangePasswordRequest, UserUpdateRequest

logger = logging.getLogger(__name__)


class UserService:
    """Business logic for user profile management."""

    def __init__(self, db: Session) -> None:
        self._repo = UserRepository(db)

    def get_profile(self, user_id: str) -> dict:
        """Return the public profile of a user."""
        user = self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return self._user_to_dict(user)

    def update_profile(self, user_id: str, request: UserUpdateRequest) -> dict:
        """Update a user's profile fields."""
        user = self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        update_data = request.model_dump(exclude_unset=True)
        if not update_data:
            return self._user_to_dict(user)

        user = self._repo.update(user, **update_data)
        logger.info("User profile updated: %s", user.id)
        return self._user_to_dict(user)

    def change_password(
        self,
        user_id: str,
        request: ChangePasswordRequest,
    ) -> None:
        """Verify current password and set a new one."""
        user = self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        if not verify_password(request.current_password, user.password_hash):
            raise ValidationError("Current password is incorrect")

        new_hash = hash_password(request.new_password)
        self._repo.update(user, password_hash=new_hash)
        logger.info("Password changed for user: %s", user.id)

    def get_all_users(self, page: int = 1, limit: int = 20) -> dict:
        """Return a paginated list of all users (admin only)."""
        skip = (page - 1) * limit
        users = self._repo.get_all(skip=skip, limit=limit)
        total = self._repo.count()
        return {
            "items": [self._user_to_dict(u) for u in users],
            "total": total,
            "page": page,
            "limit": limit,
        }

    def update_role(self, user_id: str, new_role: str) -> dict:
        """Change a user's role (admin only)."""
        user = self._repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        user = self._repo.update(user, role=new_role)
        logger.info("User role updated: %s -> %s", user.id, new_role)
        return self._user_to_dict(user)

    @staticmethod
    def _user_to_dict(user) -> dict:
        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at.isoformat(),
        }
