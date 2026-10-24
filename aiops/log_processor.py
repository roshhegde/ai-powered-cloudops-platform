import json

from aiops.analyzer import analyze_log


def process_log_line(log_line):
    """
    Parse a JSON log line and analyze HTTP request events.
    """
    try:
        log_event = json.loads(log_line)
    except (json.JSONDecodeError, TypeError):
        return {
            "classification": "INVALID_LOG",
            "severity": "UNKNOWN",
            "summary": "Log line is not valid JSON.",
            "suggested_action": "Check the log format."
        }

    if not isinstance(log_event, dict):
        return {
            "classification": "INVALID_LOG",
            "severity": "UNKNOWN",
            "summary": "Expected a JSON object.",
            "suggested_action": "Check the log format."
        }

    if log_event.get("event") != "http_request":
        return {
            "classification": "IGNORED",
            "severity": "INFO",
            "summary": "Log is not an HTTP request event.",
            "suggested_action": "No action required."
        }

    return analyze_log(log_event)