"""Shared FastAPI dependencies."""

from __future__ import annotations

from functools import lru_cache

from fastapi import Request

from app.config.settings import Settings, settings as _settings


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return _settings


def get_request_id(request: Request) -> str:
    """Extract or generate a unique request identifier."""
    return request.headers.get("X-Request-ID", "")
