"""Tests for the API endpoints.

These run in CI on every push. If an endpoint breaks, the pipeline fails
and the bad code is caught before it ever ships.
"""
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_root_returns_service_info():
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"] == "devops-pipeline-demo"
    assert "version" in body
