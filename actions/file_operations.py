from flask import request
import os
import ast
import shutil  # Module for copying and moving files
from func_utils import resolve_path, commit_changes

@commit_changes("commitMessage")
def file_operations_action():
    """Action handler for basic file operations."""
    operation = request.args.get('operation')
    path = request.args.get('path')
    target_path = request.args.get('targetPath', None)  # For copy, move, or rename
    encoding = request.args.get('encoding', 'utf-8')
    content = request.args.get('content', None)
    commit_message = request.args.get('commitMessage')

    if not operation or not path:
        return {"error": "The 'operation' and 'path' parameters are required."}, 400

    try:
        resolved_path = resolve_path(path)

        if operation == 'read':
            # No commit message required for reading
            if not os.path.isfile(resolved_path):
                return {"error": "File not found."}, 404

            with open(resolved_path, 'r', encoding=encoding) as file:
                return {"content": file.read()}, 200

        elif operation == 'write':
            # Require commitMessage for write
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for writing."}, 400

            if not content:
                return {"error": "The 'content' parameter is required for writing."}, 400
            
            if path.endswith(".py"):
                _, _, main_guard_found = detect_blocking_functions(content)
                if not(main_guard_found):
                    return {"error": f"\nif __name__ == '__main__:' not found"}, 400

            with open(resolved_path, 'w', encoding=encoding) as file:
                file.write(content)
            return {"message": "File written successfully."}, 202

        elif operation == 'delete':
            # Require commitMessage for delete
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for deleting."}, 400

            if not os.path.isfile(resolved_path):
                return {"error": "File not found."}, 404

            os.remove(resolved_path)
            return {"message": "File deleted successfully."}, 202

        elif operation == 'rename':
            # Require commitMessage for rename
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for renaming."}, 400

            if not target_path:
                return {"error": "The 'targetPath' parameter is required for renaming."}, 400

            target_resolved_path = resolve_path(target_path)
            os.rename(resolved_path, target_resolved_path)
            return {"message": "File renamed successfully."}, 202

        elif operation == 'move':
            # Require commitMessage for move
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for moving."}, 400

            if not target_path:
                return {"error": "The 'targetPath' parameter is required for moving."}, 400

            target_resolved_path = resolve_path(target_path)
            shutil.move(resolved_path, target_resolved_path)
            return {"message": "File moved successfully."}, 202

        elif operation == 'copy':
            # Require commitMessage for copy
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for copying."}, 400

            if not target_path:
                return {"error": "The 'targetPath' parameter is required for copying."}, 400

            target_resolved_path = resolve_path(target_path)
            shutil.copy(resolved_path, target_resolved_path)
            return {"message": "File copied successfully."}, 202

        else:
            return {"error": f"Unsupported operation '{operation}'."}, 400

    except (IOError, UnicodeDecodeError, OSError) as e:
        return {"error": str(e)}, 500

def detect_blocking_functions(content):
    """
    Detects blocking functions and the presence of 'if __name__ == "__main__":' 
    in the given Python code content using AST.

    Args:
        content (str): The Python code content.

    Returns:
        dict: A dictionary with keys:
            - "blocking_found" (bool): True if blocking functions are found, False otherwise.
            - "blocking_functions" (list): A list of detected blocking function names.
            - "main_guard_found" (bool): True if 'if __name__ == "__main__":' is found, False otherwise.
    """
    blocking_functions = {"input"}  # Add more blocking functions as needed
    detected_blocking_calls = []
    main_guard_found = False

    try:
        # Parse the content into an AST
        tree = ast.parse(content)

        # Walk through the AST nodes
        for node in ast.walk(tree):
            # Look for function calls
            if isinstance(node, ast.Call):
                # Check if the function is a simple name (like "input")
                if isinstance(node.func, ast.Name):
                    if node.func.id in blocking_functions:
                        detected_blocking_calls.append(node.func.id)
                # Check if the function is a dotted name (like "time.sleep")
                elif isinstance(node.func, ast.Attribute):
                    if isinstance(node.func.value, ast.Name) and f"{node.func.value.id}.{node.func.attr}" in blocking_functions:
                        detected_blocking_calls.append(f"{node.func.value.id}.{node.func.attr}")
            
            # Detect 'if __name__ == "__main__":'
            if isinstance(node, ast.If):
                if (
                    isinstance(node.test, ast.Compare) and
                    isinstance(node.test.left, ast.Name) and
                    node.test.left.id == "__name__" and
                    isinstance(node.test.ops[0], ast.Eq) and
                    isinstance(node.test.comparators[0], ast.Constant) and
                    node.test.comparators[0].value == "__main__"
                ):
                    main_guard_found = True

        return bool(detected_blocking_calls), detected_blocking_calls, main_guard_found

    except Exception as e:
        print(f"Error processing content: {e}")
        return False, [], False