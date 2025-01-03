from pathlib import Path
from flask import request
import subprocess
import os
from config import START_DIR

def commit_changes(commit_message_key):
    """Decorator to automatically commit changes after a file operation."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Resolve the repository path and ensure it is a Git repository
            repo_path = resolve_path("")  # Assuming the current directory is the repo
            try:
                # Check if the directory is a Git repository
                git_dir = os.path.join(repo_path, ".git")
                if not os.path.isdir(git_dir):
                    ensure_git_repo(repo_path)
            except RuntimeError as e:
                return {"error": str(e)}, 500

            # Perform the operation
            response, status_code = func(*args, **kwargs)

            if status_code == 202:  # Only commit if the operation was successful
                # Extract the commit message from kwargs
                commit_message = request.get_json().get(commit_message_key)
                if not commit_message:
                    return {"error": f"The '{commit_message_key}' parameter is required."}, 400
                try:
                    # Perform the add operation
                    subprocess.run(
                        ["git", "add", "."],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        check=True
                    )

                    # Check if there are staged changes
                    diff_result = subprocess.run(
                        ["git", "diff", "--cached", "--name-only"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    if diff_result.stdout.strip():
                        # Commit the changes
                        subprocess.run(["git", "commit", "-m", commit_message, "--author", "GPTCoAssistant <>"], cwd=repo_path, check=True, text=True)

                    # Retrieve the commit SHA
                    result = subprocess.run(
                        ["git", "rev-parse", "HEAD"],
                        cwd=repo_path,
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    commit_sha = result.stdout.strip()
                    response["commit_sha"] = commit_sha  # Add the SHA to the response

                except subprocess.CalledProcessError as e:
                    response["warning"] = f"Git operation failed: {str(e)}"

            return response, 200
        return wrapper

    return decorator

def ensure_git_repo(path):
    """Ensure the directory is a Git repository, initialize if not."""
    try:
        # Initialize Git repository
        subprocess.run(["git", "init"], cwd=path, check=True, text=True)

        # Create a .gitignore file if it doesn't exist
        gitignore_path = os.path.join(path, ".gitignore")
        if not os.path.exists(gitignore_path):
            with open(gitignore_path, "w") as gitignore_file:
                gitignore_file.write("logs/\n")  # Add rule to ignore the entire logs folder

        # Stage all existing files and create an initial commit
        subprocess.run(["git", "add", "."], cwd=path, check=True, text=True)
        subprocess.run(["git", "commit", "-m", "Initial commit", "--author", "GPTCoAssistant <>"], cwd=path, check=True, text=True)

    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git operation failed: {e}")

def resolve_path(path):
    """Resolve the path relative to START_DIR."""
    START_DIR_resolved = Path(f"./{START_DIR}").resolve()
    path_resolved = Path(f"./{START_DIR}/{path}").resolve()
    if path_resolved.is_relative_to(START_DIR_resolved):
        return f"./{START_DIR}/{path}"
    else:
        return f"./{START_DIR}"
