#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

from loguru import logger

from app.core.logging import configure_logging


def test_logger_initializes():
    """Test that the logger is initialized correctly."""
    configure_logging()
    logger.info("Test log message")
