import os
import re
from flask import request
from func_utils import resolve_path

def list_files_in_directory(path, recursive=True, file_path_regex=None, grep_regex=None, list_directories=False):
    results = []
    try:
        for root, dirs, files in os.walk(path):
            if not recursive:
                dirs.clear()

            entries = dirs if list_directories else files
            for entry in entries:
                entry_path = os.path.join(root, entry)
                relative_path = os.path.relpath(entry_path, path)

                if file_path_regex and not re.search(file_path_regex, relative_path):
                    continue

                if grep_regex and not list_directories:
                    try:
                        with open(entry_path, 'r') as file:
                            if not any(re.search(grep_regex, line) for line in file):
                                continue
                    except (IOError, UnicodeDecodeError):
                        continue

                results.append(relative_path)
    except Exception as e:
        return {"error": str(e)}

    return results

def list_files_action():
    """Action handler for the /listFiles endpoint."""
    path = resolve_path(request.args.get('path', '.'))
    recursive = request.args.get('recursive', 'true').lower() == 'true'
    file_path_regex = request.args.get('filePathRegex')
    grep_regex = request.args.get('grepRegex')
    list_directories = request.args.get('listDirectories', 'false').lower() == 'true'

    result = list_files_in_directory(
        path=path,
        recursive=recursive,
        file_path_regex=file_path_regex,
        grep_regex=grep_regex,
        list_directories=list_directories
    )

    if isinstance(result, dict) and "error" in result:
        return result, 500
    elif len(result) == 0:
        return "Empty root folder", 200
    return '\n'.join(result), 200
