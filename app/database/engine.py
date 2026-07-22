"""SQLAlchemy database engine configuration and lifecycle."""

from __future__ import annotations

import logging

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool

from app.config.settings import settings

logger = logging.getLogger(__name__)

engine: Engine = create_engine(
    url=settings.database_url,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=settings.DATABASE_POOL_PRE_PING,
    poolclass=QueuePool,
)


def check_database_connection() -> bool:
    """Verify database connectivity with a lightweight query."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connection verified")
        return True
    except Exception:
        logger.exception("Database connection check failed")
        return False


def dispose_database_engine() -> None:
    """Dispose of the database engine and release all connections."""
    engine.dispose()
    logger.info("Database engine disposed")
