import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pytest
from fastapi.testclient import TestClient
from backend.app.api.app import app
from backend.app.api.deps import set_engine
from backend.app.core.engine import Engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_engine():
    # Fresh engine for clean test isolation
    test_engine = Engine()
    set_engine(test_engine)
    return test_engine


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["success"] is True
    assert "data" in json_data
    assert json_data["data"]["application_status"] == "healthy"
    assert "uptime_seconds" in json_data["data"]
    assert json_data["request_id"] != ""
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers


def test_version_endpoint():
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["success"] is True
    assert json_data["data"]["app_name"] == "AtherOS"
    assert json_data["data"]["environment"] in ("development", "testing", "production")


def test_goals_execute_endpoint():
    payload = {"goal": "Read project documents and list files"}
    response = client.post("/api/v1/goals/execute", json=payload)
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["success"] is True
    data = json_data["data"]
    assert data["goal"] == "Read project documents and list files"
    assert data["status"] == "COMPLETED"
    assert len(data["tasks"]) > 0
    assert "session_id" in data


def test_chat_endpoint():
    payload = {"message": "Hello AtherOS agent"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["success"] is True
    data = json_data["data"]
    assert data["status"] == "COMPLETED"
    assert "session_id" in data


def test_get_session_by_id_endpoint():
    # First execute a goal to populate a session
    exec_resp = client.post("/api/v1/goals/execute", json={"goal": "Session lookup goal"})
    session_id = exec_resp.json()["data"]["session_id"]

    response = client.get(f"/api/v1/sessions/{session_id}")
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["success"] is True
    data = json_data["data"]
    assert data["session_id"] == session_id
    assert data["state"] == "COMPLETED"


def test_get_task_by_id_endpoint():
    # First execute a goal to produce tasks
    exec_resp = client.post("/api/v1/goals/execute", json={"goal": "Task lookup file test"})
    tasks = exec_resp.json()["data"]["tasks"]
    task_id = tasks[0]["task_id"]

    response = client.get(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200
    json_data = response.json()

    assert json_data["success"] is True
    data = json_data["data"]
    assert data["task_id"] == task_id
    assert data["status"] == "COMPLETED"


def test_validation_error_format():
    # Invalid request body (missing required field 'goal')
    response = client.post("/api/v1/goals/execute", json={})
    assert response.status_code == 422
    json_data = response.json()

    assert json_data["success"] is False
    assert json_data["error_code"] == "VALIDATION_ERROR"
    assert "request_id" in json_data


def test_not_found_error_format():
    response = client.get("/api/v1/sessions/non_existent_session_id_12345")
    assert response.status_code == 404
    json_data = response.json()

    assert json_data["success"] is False
    assert json_data["error_code"] == "HTTP_ERROR"
    assert "request_id" in json_data
