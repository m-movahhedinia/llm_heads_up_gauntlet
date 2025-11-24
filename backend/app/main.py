#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from fastapi import FastAPI

from app.obs.server import prom_app
from app.obs.tracing import setup_tracing


def create_app():
    setup_tracing()
    app = FastAPI(title="WordGame Backend")
    app.mount("/metrics", prom_app)  # Prometheus endpoint
    # include existing routers...
    return app


app = create_app()
