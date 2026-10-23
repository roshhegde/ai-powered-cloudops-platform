
from aiops.log_processor import process_log_line


def test_processes_server_error_log():
    log_line = (
        '{"event":"http_request","path":"/api/orders",'
        '"status_code":500,"duration_ms":25.0}'
    )

    result = process_log_line(log_line)

    assert result["classification"] == "SERVER_ERROR"
    assert result["severity"] == "HIGH"
    assert result["path"] == "/api/orders"


def test_rejects_invalid_json():
    result = process_log_line("this is not valid JSON")

    assert result["classification"] == "INVALID_LOG"
    assert result["severity"] == "UNKNOWN"


def test_ignores_non_http_events():
    log_line = '{"event":"application_startup"}'

    result = process_log_line(log_line)

    assert result["classification"] == "IGNORED"
    assert result["severity"] == "INFO"


def test_rejects_json_array():
    result = process_log_line('[1, 2, 3]')

    assert result["classification"] == "INVALID_LOG"