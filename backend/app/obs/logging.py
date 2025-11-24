#!/usr/bin/env python3
"""Author: mansour

Description:

"""

import os
import sys

from loguru import logger


def setup_logging():
    level = os.getenv("LOG_LEVEL", "INFO")
    logger.remove()
    logger.add(sys.stderr, level=level, backtrace=False, diagnose=False, format="{time} {level} {message}")
