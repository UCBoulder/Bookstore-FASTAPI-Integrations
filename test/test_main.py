import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def app(monkeypatch):
    """patch in our env vars required for pydantic settings"""
    monkeypatch.setenv("GRAPHQL_KEY", "test")
    monkeypatch.setenv("BASIC_USERNAME", "test")
    monkeypatch.setenv("BASIC_PASSWORD", "test")

    # import app after patching env vars
    from app.main import app

    return app


@pytest.fixture()
def client(app):
    return TestClient(app)


def test_root(client):
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_ready(client):
    response = client.get("/ready")
    assert response.status_code == 200
    assert "Hello" in response.json().keys()
