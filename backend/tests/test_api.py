import pytest
from fastapi.testclient import TestClient
from agentforge.backend.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

def test_read_main():
    # Basic check to see if API starts
    response = client.get("/")
    assert response.status_code in [200, 404] # 404 is fine if no root route defined

@patch("agentforge.backend.main.manager.broadcast")
def test_create_task(mock_broadcast):
    response = client.post("/api/tasks?title=Test%20Task&repo=org/repo")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["repo"] == "org/repo"
    assert "id" in data
    mock_broadcast.assert_called_once()

def test_get_task_logs_empty():
    response = client.get("/api/tasks/nonexistent/logs")
    assert response.status_code == 200
    assert response.json() == {"logs": []}
