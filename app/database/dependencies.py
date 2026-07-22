"""FastAPI dependency injection for database sessions.

Provides a ``get_db`` dependency that yields a SQLAlchemy session
and automatically commits on success or rolls back on failure.
"""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy.orm import Session as SaSession

from app.database.session import SessionLocal


def get_db() -> Generator[SaSession, None, None]:
    """FastAPI dependency that provides a database session.

    Usage::

        @router.get("/items")
        def list_items(db: Session = Depends(get_db)):
            ...

    The session is committed on successful completion and
    rolled back if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
