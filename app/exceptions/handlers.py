"""Custom exceptions and global FastAPI exception handlers."""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class AppException(Exception):
    """Base exception for all application-level errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(AppException):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", code: str = "NOT_FOUND") -> None:
        super().__init__(message=message, code=code, status_code=404)


class ValidationError(AppException):
    """Raised when input validation fails at the application level."""

    def __init__(self, message: str = "Validation failed", code: str = "VALIDATION_ERROR") -> None:
        super().__init__(message=message, code=code, status_code=422)


class ConflictError(AppException):
    """Raised when a resource conflict occurs."""

    def __init__(self, message: str = "Resource conflict", code: str = "CONFLICT") -> None:
        super().__init__(message=message, code=code, status_code=409)


class UnauthorizedError(AppException):
    """Raised when authentication is required or fails."""

    def __init__(self, message: str = "Unauthorized", code: str = "UNAUTHORIZED") -> None:
        super().__init__(message=message, code=code, status_code=401)


def _error_response(message: str, code: str, details: str | None = None) -> dict:
    """Build a standardized error response body."""
    body: dict = {
        "success": False,
        "message": message,
        "error": {"code": code},
    }
    if details:
        body["error"]["details"] = details
    return body


async def app_exception_handler(request: Request, exc: AppException) -> dict:
    """Handle custom AppException subclasses."""
    logger.warning("AppException: %s (%s)", exc.message, exc.code)
    return _error_response(message=exc.message, code=exc.code)


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> dict:
    """Handle Starlette HTTP exceptions."""
    logger.warning("HTTPException: %s", exc.detail)
    return _error_response(message=exc.detail, code=f"HTTP_{exc.status_code}")


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> dict:
    """Handle FastAPI request validation errors."""
    logger.warning("ValidationError: %s", exc.errors())
    return _error_response(
        message="Request validation failed",
        code="VALIDATION_ERROR",
        details=str(exc.errors()),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> dict:
    """Catch-all for unhandled exceptions."""
    logger.exception("Unhandled exception: %s", exc)
    return _error_response(
        message="An internal error occurred",
        code="INTERNAL_ERROR",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all global exception handlers on the FastAPI application."""
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
