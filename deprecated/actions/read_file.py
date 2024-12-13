from flask import request
import os
from func_utils import resolve_path

def read_file_action():
    """Action handler for the /readFile endpoint."""

    path = request.args.get('path')
    encoding = request.args.get('encoding', 'utf-8')
    max_bytes = request.args.get('maxBytes', None)

    if not path:
        return {"error": "The 'path' parameter is required."}, 400

    try:
        resolved_path = resolve_path(path)

        if not os.path.isfile(resolved_path):
            return {"error": "File not found."}, 404

        with open(resolved_path, 'r', encoding=encoding) as file:
            if max_bytes:
                try:
                    max_bytes = int(max_bytes)
                    content = file.read(max_bytes)
                except ValueError:
                    return {"error": "Invalid value for 'maxBytes'. Must be an integer."}, 400
            else:
                content = file.read()

        return content, 200

    except (IOError, UnicodeDecodeError) as e:
        return {"error": str(e)}, 500
