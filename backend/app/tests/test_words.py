#!/usr/bin/env python3
"""
Author: mansour

Description:

"""

from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)


def test_get_curated_words():
    resp = client.get("/api/v1/words/curated")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert "text" in data[0]


def test_get_random_word():
    resp = client.get("/api/v1/words/random")
    assert resp.status_code == 200
    data = resp.json()
    assert "text" in data
