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

        # if request.path not in ["/openapi.json", "/openapi.yaml"]:
        #     if response.status_code == 200:
        #         # Handle response data (always JSON)
        #         response_data = response.get_json(silent=True) or {}
        #         if isinstance(response_data, dict):
        #             # Add the reminder instruction to the response
        #             response_data["instruction_reminder"] = (
        #                 "Remember the instructions in 'GPT_Instructions.md'. "
        #                 "Start the next response with 'Pre-Action Confirmation and Preparation' and "
        #                 "follow the response structure as specified."
        #             )
        #             # Modify the response to include the updated response data
        #             response.set_data(json.dumps(response_data, indent=2))

        if request.path not in ignored_endpoints:
            # Initialize the log entry with common details
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "method": request.method,
                "url": request.url,
                "status_code": response.status_code
            }

            # Handle response data (always JSON)
            response_data = response.get_json(silent=True) or {}
            if isinstance(response_data, dict):
                response_data.pop("content", None)
            log_entry["response_data"] = json.dumps(response_data)

            # Handle request data (always JSON)
            request_data = request.get_json(silent=True) or {}
            if isinstance(request_data, dict):
                request_data.pop("content", None)
                request_data.pop("assistantLastResponse", None)
            log_entry["body"] = json.dumps(request_data)

            if not(os.path.isdir(LOG_DIR)):
                os.makedirs(LOG_DIR, exist_ok=True)

            # Save log to file
            log_file = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")

        return response
