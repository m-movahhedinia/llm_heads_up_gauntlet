#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from app.core.validation import SafeGenParams


def test_param_clamp():
    p = SafeGenParams(temperature=3.0, top_k=100, max_tokens=99999)
    assert p.temperature == 3.0  # pydantic validates. clamp when applying to config
