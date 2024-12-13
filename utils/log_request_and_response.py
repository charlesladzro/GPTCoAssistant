import json
from datetime import datetime
import os
from flask import request
from func_utils import resolve_path

# Directory to store logs
LOG_DIR = resolve_path("logs")

def log_request_and_response(app):
    """Middleware to log request and response."""

    @app.before_request
    def before_request():
        request.start_time = datetime.now()

    @app.after_request
    def after_request(response):
        # List of endpoints to ignore
        ignored_endpoints = ["/log_operations", "/openapi.json", "/openapi.yaml"]

        if request.path not in ignored_endpoints:
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "url": request.url,
                "body": request.get_data(as_text=True),
                "status_code": response.status_code,
                "response_data": response.get_data(as_text=True),
            }

            if not(os.path.isdir(LOG_DIR)):
                os.makedirs(LOG_DIR, exist_ok=True)

            # Save log to file
            log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")

        return response
