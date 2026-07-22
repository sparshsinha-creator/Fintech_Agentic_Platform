"""User repository for database operations."""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    """Handles persistence operations for the User model."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_id(self, user_id: str) -> User | None:
        """Return a user by their UUID primary key."""
        return self._db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        """Return a user by their email address."""
        return self._db.query(User).filter(User.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 20) -> list[User]:
        """Return a paginated list of all users."""
        return self._db.query(User).offset(skip).limit(limit).all()

    def create(self, **kwargs) -> User:
        """Create and persist a new user."""
        user = User(**kwargs)
        self._db.add(user)
        self._db.flush()
        return user

    def update(self, user: User, **kwargs) -> User:
        """Update an existing user's attributes in-place."""
        for key, value in kwargs.items():
            setattr(user, key, value)
        self._db.flush()
        return user

    def count(self) -> int:
        """Return the total number of users."""
        return self._db.query(User).count()
