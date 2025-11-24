#!/usr/bin/env python3
"""Author: mansour

Description:

"""


# TODO Make this configurable
def redact(text: str, max_len: int = 500) -> str:
    t = text.replace("OPENAI_API_KEY", "[REDACTED]")
    return t[:max_len] + ("..." if len(t) > max_len else "")
