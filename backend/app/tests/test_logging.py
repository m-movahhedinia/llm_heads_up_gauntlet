#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

from app.core.logging import configure_logging
from loguru import logger


def test_logger_initializes():
    """Test that the logger is initialized correctly."""
    configure_logging()
    logger.info("Test log message")
