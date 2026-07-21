"""
FastAPI application entry point.

Initializes the FastAPI application and registers
routers, middleware, exception handlers, and lifecycle events.

Business logic must not be placed here.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.config.logging import setup_logging
from app.config.settings import settings
from app.exceptions.handlers import register_exception_handlers

logger = logging.getLogger(__name__)


def create_application() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    setup_logging()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI Financial Intelligence Platform",
        docs_url="/docs" if settings.is_development else None,
        redoc_url="/redoc" if settings.is_development else None,
    )

    app.include_router(api_router)
    register_exception_handlers(app)

    logger.info("Application started", extra={"version": settings.APP_VERSION, "env": settings.APP_ENV})

    return app


app = create_application()
