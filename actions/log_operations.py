import os
import json
from flask import request
from func_utils import resolve_path

def log_operations_action():
    """Retrieve logs based on filters."""
    # Parse JSON body for POST requests
    data = request.get_json()
    if not data:
        return {"error": "Invalid or missing JSON body."}, 400
    
    log_dir = resolve_path("logs")
    date_filter = data.get("date")  # YYYY-MM-DD format
    assistantLastResponse = data.get("assistantLastResponse")

    if not assistantLastResponse or "Pre-Action Confirmation and Preparation" not in assistantLastResponse:
        return {"error": "You have not followed the 'Persistent Response Structure' and not starting your last response by 'Pre-Action Confirmation and Preparation' as specified. If you are not familiar with it, please read the file 'GPT_Instructions.md' in root folder. In the file, READ carefully the recommandation about 'assistantLastResponse'."}, 400
    
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
