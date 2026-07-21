"""Logging configuration for the MyFinance platform."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from app.config.settings import settings


def setup_logging() -> None:
    """Configure application-wide logging.

    Sets up both console and file handlers based on the
    LOG_LEVEL and LOG_FILE_PATH settings.
    """
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(_create_formatter())
    root_logger.addHandler(console_handler)

    if settings.LOG_FILE_PATH:
        log_path = Path(settings.LOG_FILE_PATH)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(log_level)
        file_handler.setFormatter(_create_formatter())
        root_logger.addHandler(file_handler)

    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        _quiet_logger(logger_name, log_level)

    logging.getLogger(__name__).info(
        "Logging initialized", extra={"level": settings.LOG_LEVEL, "file": settings.LOG_FILE_PATH}
    )


def _create_formatter() -> logging.Formatter:
    """Create a log formatter."""
    return logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def _quiet_logger(logger_name: str, level: int) -> None:
    """Set a named logger to the given level and suppress propagation if needed."""
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.propagate = True
