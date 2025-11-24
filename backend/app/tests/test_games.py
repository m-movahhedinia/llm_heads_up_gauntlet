#!/usr/bin/env python3
"""Author: mansour

Description:

"""

from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_start_game():
    resp = client.post("/api/v1/games/start")
    assert resp.status_code == 200
    data = resp.json()
    assert data["text"] == "logic"


def test_submit_round():
    resp = client.post("/api/v1/games/rounds/1/submit")
    assert resp.status_code == 200
    data = resp.json()
    assert data["correct"] is True
