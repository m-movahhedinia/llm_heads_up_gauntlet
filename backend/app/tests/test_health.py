#!/usr/bin/env python3
"""Author: mansour.

Description:

"""

from app.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_ok():
    """Test that the health endpoint returns a 200 OK response."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_root_message():
    """Test that the root endpoint returns a message."""
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert "Backend is running" in data["message"]
