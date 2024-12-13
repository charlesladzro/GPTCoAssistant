from flask import request
import os
import subprocess  # Permet d'exécuter des commandes shell
from func_utils import resolve_path

def git_operations_action():
    """Action handler for basic Git operations."""
    
    operation = request.args.get('operation')
    repo_path = request.args.get('repoPath')
    remote_url = request.args.get('remoteUrl', None)
    branch_name = request.args.get('branchName', None)
    commit_message = request.args.get('commitMessage', None)
    target_path = request.args.get('targetPath', None)  # Pour clone
    files = request.args.get('files', None)  # Pour add
    resolved_repo_path = resolve_path(repo_path) if repo_path else None

    if not operation:
        return {"error": "The 'operation' parameter is required."}, 400

    try:
        if operation == 'clone':
            if not remote_url or not target_path:
                return {"error": "The 'remoteUrl' and 'targetPath' parameters are required for cloning."}, 400

            resolved_target_path = resolve_path(target_path)
            result = subprocess.run(["git", "clone", remote_url, resolved_target_path], capture_output=True, text=True)
            return get_response(result)

        elif operation == 'pull':
            if not resolved_repo_path:
                return {"error": "The 'repoPath' parameter is required for pulling."}, 400

            result = subprocess.run(["git", "pull"], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        elif operation == 'add':
            if not resolved_repo_path:
                return {"error": "The 'repoPath' parameter is required for adding files."}, 400

            add_files = files.split() if files else ["."]
            result = subprocess.run(["git", "add", *add_files], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        elif operation == 'commit':
            if not resolved_repo_path or not commit_message:
                return {"error": "The 'repoPath' and 'commitMessage' parameters are required for committing."}, 400

            result = subprocess.run(["git", "commit", "-m", commit_message], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        elif operation == 'push':
            if not resolved_repo_path:
                return {"error": "The 'repoPath' parameter is required for pushing."}, 400

            result = subprocess.run(["git", "push"], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        elif operation == 'branch':
            if not resolved_repo_path:
                return {"error": "The 'repoPath' parameter is required for branch operations."}, 400

            if branch_name:
                result = subprocess.run(["git", "branch", branch_name], cwd=resolved_repo_path, capture_output=True, text=True)
            else:
                result = subprocess.run(["git", "branch"], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        elif operation == 'checkout':
            if not resolved_repo_path or not branch_name:
                return {"error": "The 'repoPath' and 'branchName' parameters are required for checkout."}, 400

            result = subprocess.run(["git", "checkout", branch_name], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        elif operation == 'status':
            if not resolved_repo_path:
                return {"error": "The 'repoPath' parameter is required for status."}, 400

            result = subprocess.run(["git", "status"], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        elif operation == 'log':
            if not resolved_repo_path:
                return {"error": "The 'repoPath' parameter is required for log."}, 400

            result = subprocess.run(["git", "log"], cwd=resolved_repo_path, capture_output=True, text=True)
            return get_response(result)

        else:
            return {"error": f"Unsupported operation '{operation}'."}, 400

    except Exception as e:
        return {"error": str(e)}, 500

def get_response(result):
    """
    Return a response based on the result's return code.

    Args:
        result: An object with attributes stdout, stderr, and returncode.

    Returns:
        A dictionary containing a message or error and an HTTP status code.
    """
    if result.returncode == 0:
        return {"message": result.stdout.strip()}, 200
    else:
        return {"error": result.stderr.strip()}, 500
