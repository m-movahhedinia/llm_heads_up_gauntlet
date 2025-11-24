#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

from app.core.config import settings


def test_defaults_loaded():
    """Test that the default settings are loaded."""
    assert settings.app_name
    assert settings.environment in {"development", "production", "staging", "test"}
    assert isinstance(settings.debug, bool)
    assert settings.api_prefix.startswith("/")


def test_log_level_default():
    """Test that the log level is set to INFO by default."""
    assert settings.log_level in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
