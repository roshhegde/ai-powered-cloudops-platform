import json
import logging
import time
from datetime import datetime, timezone

from flask import Flask, jsonify, request, g

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger("cloudops-app")


@app.before_request
def log_request_start():
    g.request_start_time = time.perf_counter()


@app.after_request
def log_request_end(response):
    start_time = getattr(g, "request_start_time", None)

    duration_ms = (
        round((time.perf_counter() - start_time) * 1000, 2)
        if start_time is not None
        else None
    )

    log_event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": "INFO" if response.status_code < 400 else "WARNING",
        "event": "http_request",
        "method": request.method,
        "path": request.path,
        "status_code": response.status_code,
        "duration_ms": duration_ms,
    }

    logger.info(json.dumps(log_event))

    return response


@app.route("/")
def home():
    return jsonify({
        "application": "AI-Powered CloudOps Platform",
        "status": "running",
        "timestamp": datetime.now(timezone.utc).isoformat()
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
