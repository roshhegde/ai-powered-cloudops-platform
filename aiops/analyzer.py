
def analyze_log(log_event):
    """
    Analyze a structured application log and classify the event.
    """

    status_code = log_event.get("status_code")
    duration_ms = log_event.get("duration_ms")
    path = log_event.get("path", "unknown")

    # Validate the fields we need.
    if not isinstance(status_code, int) or isinstance(status_code, bool):
        return {
            "classification": "INVALID_LOG",
            "severity": "UNKNOWN",
            "path": path,
            "summary": "Missing or invalid HTTP status code.",
            "suggested_action": "Check the log event format."
        }

    if duration_ms is not None and (
        not isinstance(duration_ms, (int, float))
        or isinstance(duration_ms, bool)
        or duration_ms < 0
    ):
        return {
            "classification": "INVALID_LOG",
            "severity": "UNKNOWN",
            "path": path,
            "summary": "Missing or invalid request duration.",
            "suggested_action": "Check the log event format."
        }

    # Classify the HTTP response.
    if status_code >= 500:
        classification = "SERVER_ERROR"
        severity = "HIGH"
        summary = f"Server error detected on {path}."
        suggested_action = (
            "Inspect application logs, dependencies, and server health."
        )

    elif status_code >= 400:
        classification = "CLIENT_ERROR"
        severity = "LOW"
        summary = f"Client error detected on {path}."
        suggested_action = (
            "Check the request, URL, and route configuration."
        )

    else:
        classification = "HEALTHY"
        severity = "INFO"
        summary = f"Request completed successfully on {path}."
        suggested_action = "No immediate action required."

    # Independently flag slow requests.
    if duration_ms is not None and duration_ms > 1000:
        if classification == "HEALTHY":
            classification = "SLOW_REQUEST"
            severity = "MEDIUM"

        summary += f" Request duration was {duration_ms} ms."
        suggested_action = (
            "Investigate application latency and downstream dependencies."
        )

    return {
        "classification": classification,
        "severity": severity,
        "path": path,
        "status_code": status_code,
        "duration_ms": duration_ms,
        "summary": summary,
        "suggested_action": suggested_action
    }