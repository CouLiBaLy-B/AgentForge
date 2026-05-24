import pytest
from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code in [200, 404]

@patch("backend.main.manager.broadcast")
def test_create_task(mock_broadcast):
    response = client.post("/api/tasks?title=Test%20Task&repo=org/repo")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    mock_broadcast.assert_called()
