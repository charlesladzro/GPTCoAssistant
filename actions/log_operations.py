import os
import json
from flask import request
from func_utils import resolve_path

def log_operations_action():
    """Retrieve logs based on filters."""
    log_dir = resolve_path("logs")
    date_filter = request.args.get("date")  # YYYY-MM-DD format
    log_file = os.path.join(log_dir, f"{date_filter}.log") if date_filter else None

    try:
        if log_file and os.path.isfile(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                logs = [json.loads(line) for line in f]
        else:
            # Fetch all logs
            logs = []
            for file_name in os.listdir(log_dir):
                if file_name.endswith(".log"):
                    with open(os.path.join(log_dir, file_name), "r", encoding="utf-8") as f:
                        logs.extend(json.loads(line) for line in f)

        return {"logs": logs}, 200
    except Exception as e:
        return {"error": str(e)}, 500
