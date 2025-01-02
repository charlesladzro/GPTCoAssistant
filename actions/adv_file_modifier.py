from flask import request
import os
import re
from func_utils import resolve_path, commit_changes

@commit_changes("commitMessage")
def adv_file_modifier_action():
    """
    Optimized Action handler for advanced file modification operations.
    Supports incremental updates and chunk-based processing.
    Supported operations:
    - replace: Replace all occurrences of a string with another string.
    - line_replace: Replace a specific line in the file.
    - regex_replace: Perform regex-based replacement.
    - append: Append a string to the end of the file.
    - prepend: Prepend a string to the beginning of the file.
    - batch_process: Perform operations across multiple files in a directory.
    """
    data = request.get_json()
    if not data:
        return {"error": "Invalid or missing JSON body."}, 400

    operation = data.get("operation")
    path = data.get("path")
    commit_message = data.get("commitMessage")
    search_str = data.get("searchStr")
    replace_str = data.get("replaceStr")
    line_number = data.get("lineNumber")
    new_line = data.get("newLine")
    pattern = data.get("pattern")

    if not operation or not path:
        return {"error": "The 'operation' and 'path' fields are required in the request body."}, 400

    if operation in ["replace", "line_replace", "regex_replace", "append", "prepend", "batch_process"]:
        if not commit_message:
            return {"error": f"The 'commitMessage' parameter is required for {operation}."}, 400

    try:
        resolved_path = resolve_path(path)

        # Process in chunks for efficient updates
        if operation == "replace":
            if not search_str or not replace_str:
                return {"error": "The 'searchStr' and 'replaceStr' fields are required for replace."}, 400

            buffer = []
            with open(resolved_path, 'r', encoding='utf-8') as file:
                for line in file:
                    buffer.append(line.replace(search_str, replace_str))

            with open(resolved_path, 'w', encoding='utf-8') as file:
                file.writelines(buffer)

            return {"message": "Replace operation completed successfully."}, 202

        elif operation == "line_replace":
            if not line_number or not new_line:
                return {"error": "The 'lineNumber' and 'newLine' fields are required for line_replace."}, 400

            buffer = []
            with open(resolved_path, 'r', encoding='utf-8') as file:
                for idx, line in enumerate(file, start=1):
                    if idx == line_number:
                        buffer.append(new_line + "\n")
                    else:
                        buffer.append(line)

            with open(resolved_path, 'w', encoding='utf-8') as file:
                file.writelines(buffer)

            return {"message": "Line replacement completed successfully."}, 202

        elif operation == "regex_replace":
            if not pattern or not replace_str:
                return {"error": "The 'pattern' and 'replaceStr' fields are required for regex_replace."}, 400

            buffer = []
            with open(resolved_path, 'r', encoding='utf-8') as file:
                for line in file:
                    buffer.append(re.sub(pattern, replace_str, line))

            with open(resolved_path, 'w', encoding='utf-8') as file:
                file.writelines(buffer)

            return {"message": "Regex replace operation completed successfully."}, 202

        elif operation == "append":
            if not search_str:
                return {"error": "The 'searchStr' field is required for append."}, 400

            with open(resolved_path, 'a', encoding='utf-8') as file:
                file.write(search_str + "\n")

            return {"message": "Append operation completed successfully."}, 202

        elif operation == "prepend":
            if not search_str:
                return {"error": "The 'searchStr' field is required for prepend."}, 400

            buffer = [search_str + "\n"]
            with open(resolved_path, 'r', encoding='utf-8') as file:
                buffer.extend(file.readlines())

            with open(resolved_path, 'w', encoding='utf-8') as file:
                file.writelines(buffer)

            return {"message": "Prepend operation completed successfully."}, 202

        elif operation == "batch_process":
            if not os.path.isdir(resolved_path):
                return {"error": "The specified path is not a directory."}, 400

            for filename in os.listdir(resolved_path):
                file_full_path = os.path.join(resolved_path, filename)
                if os.path.isfile(file_full_path) and filename.endswith(".txt"):
                    buffer = []
                    with open(file_full_path, 'r', encoding='utf-8') as file:
                        for line in file:
                            buffer.append(line.replace(search_str, replace_str))
                    with open(file_full_path, 'w', encoding='utf-8') as file:
                        file.writelines(buffer)

            return {"message": "Batch process operation completed successfully."}, 202

        else:
            return {"error": f"Unsupported operation '{operation}'."}, 400

    except Exception as e:
        return {"error": str(e)}, 500