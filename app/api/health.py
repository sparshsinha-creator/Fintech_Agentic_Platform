"""Health check endpoint for the MyFinance API."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.config.settings import Settings
from app.core.dependencies import get_settings
from app.database.engine import check_database_connection

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check(settings: Settings = Depends(get_settings)) -> dict:
    """Return the current health status of the application."""
    db_healthy = check_database_connection()
    status = "healthy" if db_healthy else "degraded"

    return {
        "success": True,
        "message": f"Service is {status}",
        "data": {
            "status": status,
            "version": settings.APP_VERSION,
            "environment": settings.APP_ENV,
            "database": "connected" if db_healthy else "disconnected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
