#!/usr/bin/env python3
"""
Author: mansour

Description:

"""
from prometheus_client import make_asgi_app
prom_app = make_asgi_app()