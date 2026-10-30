from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api import create_app


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(tmp_path / "todos.json"))


def test_list_starts_empty(client: TestClient) -> None:
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_add_returns_created_task(client: TestClient) -> None:
    response = client.post("/api/tasks", json={"title": "  Buy milk "})
    assert response.status_code == 201
    assert response.json() == {"task_id": 1, "title": "Buy milk", "is_done": False}
    assert client.get("/api/tasks").json() == [response.json()]


@pytest.mark.parametrize("payload", [{"title": ""}, {"title": "   "}, {}, {"title": "x" * 201}])
def test_add_rejects_invalid_titles(client: TestClient, payload: dict) -> None:
    assert client.post("/api/tasks", json=payload).status_code == 422


def test_complete_marks_task_done(client: TestClient) -> None:
    client.post("/api/tasks", json={"title": "Write report"})
    response = client.post("/api/tasks/1/complete")
    assert response.status_code == 200
    assert response.json()["is_done"] is True
    assert client.get("/api/tasks").json()[0]["is_done"] is True


def test_complete_unknown_task_is_404(client: TestClient) -> None:
    assert client.post("/api/tasks/99/complete").status_code == 404


def test_home_page_is_served(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Todo" in response.text
