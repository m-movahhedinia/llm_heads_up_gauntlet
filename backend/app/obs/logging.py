#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from loguru import logger
import os
import sys

def setup_logging():
    level = os.getenv("LOG_LEVEL", "INFO")
    logger.remove()
    logger.add(sys.stderr, level=level, backtrace=False, diagnose=False, format="{time} {level} {message}")
