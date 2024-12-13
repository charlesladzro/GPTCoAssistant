from flask import request
import os
import shutil  # Module for copying and moving files
from func_utils import resolve_path, commit_changes

@commit_changes("commitMessage")
def folder_operations_action():
    """Action handler for basic folder operations."""
    operation = request.args.get('operation')
    path = request.args.get('path')
    target_path = request.args.get('targetPath', None)  # For copy, move, or rename
    recursive = request.args.get('recursive', 'false').lower() == 'true'  # For delete and list
    commit_message = request.args.get('commitMessage')  # Commit message for relevant operations

    if not operation or not path:
        return {"error": "The 'operation' and 'path' parameters are required."}, 400

    try:
        resolved_path = resolve_path(path)

        if operation == 'create':
            # Require commitMessage for create
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for creating a folder."}, 400

            os.makedirs(resolved_path, exist_ok=True)
            return {"message": "Folder created successfully."}, 202

        elif operation == 'delete':
            # Require commitMessage for delete
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for deleting a folder."}, 400

            if not os.path.isdir(resolved_path):
                return {"error": "Folder not found."}, 404

            if recursive:
                shutil.rmtree(resolved_path)
            else:
                os.rmdir(resolved_path)
            return {"message": "Folder deleted successfully."}, 202

        elif operation == 'rename':
            # Require commitMessage for rename
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for renaming a folder."}, 400

            if not target_path:
                return {"error": "The 'targetPath' parameter is required for renaming."}, 400

            target_resolved_path = resolve_path(target_path)
            os.rename(resolved_path, target_resolved_path)
            return {"message": "Folder renamed successfully."}, 202

        elif operation == 'move':
            # Require commitMessage for move
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for moving a folder."}, 400

            if not target_path:
                return {"error": "The 'targetPath' parameter is required for moving."}, 400

            target_resolved_path = resolve_path(target_path)
            shutil.move(resolved_path, target_resolved_path)
            return {"message": "Folder moved successfully."}, 202

        elif operation == 'copy':
            # Require commitMessage for copy
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for copying a folder."}, 400

            if not target_path:
                return {"error": "The 'targetPath' parameter is required for copying."}, 400

            target_resolved_path = resolve_path(target_path)
            shutil.copytree(resolved_path, target_resolved_path)
            return {"message": "Folder copied successfully."}, 202

        elif operation == 'list':
            # No commitMessage required for list
            if not os.path.isdir(resolved_path):
                return {"error": "Folder not found."}, 404

            if recursive:
                contents = build_nested_structure(resolved_path)
                print(resolved_path)
            else:
                # Remove `.git` and `venv`
                contents = [item for item in os.listdir(resolved_path) if item not in {'.git', 'venv'}]

            if len(contents) == 0:
                return {"message": "Empty folder"}, 200
            
            return {"message": contents}, 200

        else:
            return {"error": f"Unsupported operation '{operation}'."}, 400

    except (IOError, OSError) as e:
        return {"error": str(e)}, 500

def build_nested_structure(path):
    """Helper function to build a nested structure of folder contents, skipping the .git folder."""
    result = []
    for item in os.listdir(path):
        if item == ".git"or item == "venv":
            # Skip the .git folder
            continue

        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            # Add the file directly to the list
            result.append(item)
        elif os.path.isdir(full_path):
            # Add the folder with its contents as a nested dictionary
            result.append({item: build_nested_structure(full_path)})
    return result
