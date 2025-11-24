#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

from loguru import logger

from .config import settings


def configure_logging() -> None:
    """Configure logging."""
    logger.remove()
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=settings.log_level,
        format="<level>{level}</level> | {time:YYYY-MM-DD HH:mm:ss.SSS} | {name}:{function}:{line} | {message}\n",
        colorize=True,
    )
    logger.debug("Logger initialized with level: {}", settings.log_level)
