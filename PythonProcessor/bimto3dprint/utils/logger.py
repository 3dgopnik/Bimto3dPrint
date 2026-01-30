"""Logging utilities for the pipeline.

Example:
    logger = get_logger()
    logger.info("Hello")
"""
from __future__ import annotations

from pathlib import Path
from loguru import logger

LOG_DIR = Path("Logs")
LOG_FILE = LOG_DIR / "bimto3dprint.log"


def get_logger():
    """Configure and return a shared logger instance."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.remove()
    logger.add(LOG_FILE.as_posix(), format="{time} [{level}] {message}")
    return logger
