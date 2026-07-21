"""Health check endpoint for the MyFinance API."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.config.settings import Settings
from app.core.dependencies import get_settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)) -> dict:
    """Return the current health status of the application."""
    return {
        "success": True,
        "message": "Service is healthy",
        "data": {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
