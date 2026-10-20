
from aiops.analyzer import analyze_log


def test_successful_request_is_healthy():
    result = analyze_log({
        "path": "/health",
        "status_code": 200,
        "duration_ms": 10
    })

    assert result["classification"] == "HEALTHY"
    assert result["severity"] == "INFO"


def test_server_error_is_high_severity():
    result = analyze_log({
        "path": "/api/orders",
        "status_code": 500,
        "duration_ms": 25
    })

    assert result["classification"] == "SERVER_ERROR"
    assert result["severity"] == "HIGH"


def test_client_error_is_low_severity():
    result = analyze_log({
        "path": "/unknown",
        "status_code": 404,
        "duration_ms": 3
    })

    assert result["classification"] == "CLIENT_ERROR"
    assert result["severity"] == "LOW"


def test_slow_request_is_flagged():
    result = analyze_log({
        "path": "/api/orders",
        "status_code": 200,
        "duration_ms": 1500
    })

    assert result["classification"] == "SLOW_REQUEST"
    assert result["severity"] == "MEDIUM"


def test_invalid_status_code_is_rejected():
    result = analyze_log({
        "path": "/health",
        "status_code": "invalid",
        "duration_ms": 10
    })

    assert result["classification"] == "INVALID_LOG"