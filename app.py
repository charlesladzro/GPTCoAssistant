from flask import Flask, Response
from auth import require_api_key
import os
import importlib
from openapi import get_openapi_json_endpoint, get_openapi_yaml_endpoint
from utils.log_request_and_response import log_request_and_response

app = Flask(__name__)
app.json.sort_keys = False

# Apply the logging middleware
log_request_and_response(app)

# Serve the content of README.md at the root endpoint
@app.route('/', methods=['GET'])
def serve_readme():
    """Serve the content of README.md as plain text."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:  # Specify UTF-8 encoding
            readme_content = f.read()
        return Response(readme_content, mimetype='text/plain')  # Display README as plain text
    except FileNotFoundError:
        return "README.md not found.", 404
    except UnicodeDecodeError:
        return "Failed to decode README.md. Ensure it is saved in UTF-8 encoding.", 500

# Register OpenAPI endpoints
app.add_url_rule('/openapi.json', 'get_openapi_json', get_openapi_json_endpoint, methods=['GET'])
app.add_url_rule('/openapi.yaml', 'get_openapi_yaml', get_openapi_yaml_endpoint, methods=['GET'])

# Dynamically register actions
def register_actions():
    actions_dir = "actions"
    for filename in os.listdir(actions_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{actions_dir.replace('/', '.')}.{filename[:-3]}"
            module = importlib.import_module(module_name)

            action_name = f"{filename[:-3]}_action"
            if hasattr(module, action_name):
                action_func = getattr(module, action_name)
                endpoint = f"/{filename[:-3]}"
                app.add_url_rule(endpoint, action_name, require_api_key(action_func), methods=['POST'])

register_actions()

if __name__ == '__main__':
    app.run(debug=True)
