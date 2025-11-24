#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_get_leaderboard():
    resp = client.get("/api/v1/leaderboard/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert "participant" in data[0]
