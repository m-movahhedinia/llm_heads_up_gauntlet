#!/usr/bin/env python3
"""Author: mansour.

Description:
TBD.
"""


def health_status() -> dict[str, str]:
    """Return a simple health check response.

    :return: A dictionary with a "status" key set to "ok".
    """
    return {"status": "ok"}
