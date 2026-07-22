"""Database session factory and lifecycle management."""

from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker

from app.database.engine import engine

SessionLocal: sessionmaker[Session] = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def create_session() -> Session:
    """Create a new standalone database session.

    Use this when you need manual control over commit/rollback.
    For FastAPI dependencies, prefer ``get_db`` from ``dependencies.py``.
    """
    return SessionLocal()
