
import json

from app.app import app


def test_home_endpoint():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()
    assert data["application"] == "AI-Powered CloudOps Platform"
    assert data["status"] == "running"


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_successful_request_is_logged_as_json(caplog):
    with caplog.at_level("INFO", logger="cloudops-app"):
        response = app.test_client().get("/health")

    assert response.status_code == 200

    log_records = [
        record for record in caplog.records
        if record.name == "cloudops-app"
    ]

    assert log_records, "Expected an application request log"

    log_data = json.loads(log_records[-1].message)

    assert log_data["event"] == "http_request"
    assert log_data["method"] == "GET"
    assert log_data["path"] == "/health"
    assert log_data["status_code"] == 200
    assert log_data["level"] == "INFO"
    assert isinstance(log_data["duration_ms"], (int, float))


def test_not_found_request_is_logged_as_warning(caplog):
    with caplog.at_level("INFO", logger="cloudops-app"):
        response = app.test_client().get("/unknown")

    assert response.status_code == 404

    log_records = [
        record for record in caplog.records
        if record.name == "cloudops-app"
    ]

    assert log_records, "Expected an application request log"

    log_data = json.loads(log_records[-1].message)

    assert log_data["event"] == "http_request"
    assert log_data["path"] == "/unknown"
    assert log_data["status_code"] == 404
    assert log_data["level"] == "WARNING"