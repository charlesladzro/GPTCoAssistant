from flask import request, jsonify
import subprocess
import sys
import os
import traceback
from func_utils import resolve_path, commit_changes
from config import START_DIR
from actions.file_operations import detect_blocking_functions

@commit_changes("commitMessage")
def python_operations_action():
    """Action handler for secure Python operations."""
    # Parse JSON body for POST requests
    data = request.get_json()
    if not data:
        return {"error": "Invalid or missing JSON body."}, 400
    
    operation = data.get('operation')
    script_path = data.get('scriptPath', None)  # Pour exécuter un fichier Python
    package_name = data.get('packageName', None)  # Pour pip install/uninstall
    module_name = data.get('moduleName', None)  # Pour gestion des modules
    inputs_for_test = data.get('inputs_for_test', None)
    commit_message = data.get('commitMessage', None)

    # Résolution des chemins
    script_path = resolve_path(script_path) if script_path else None
    venv_path = f"./{START_DIR}/venv"

    if not operation:
        return {"error": "The 'operation' parameter is required."}, 400

    try:
        if operation == 'create_venv':
            # Require commitMessage for create_venv
            if not commit_message:
                return {"error": "The 'commitMessage' parameter is required for venv creating."}, 400

            try:
                result = subprocess.run(
                    [sys.executable, "-m", "venv", venv_path],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return {"message": f"Virtual environment created successfully."}, 202
                else:
                    return {"stderr": result.stderr.strip()}, 500
            except Exception as e:
                return {"error": str(e), "traceback": traceback.format_exc()}, 500

        # Vérification de l'environnement virtuel
        if not venv_path or not os.path.isdir(venv_path):
            return {"error": "A valid 'venvPath' parameter is required."}, 400

        python_executable = os.path.join(venv_path, "Scripts", "python.exe")
        if not os.path.isfile(python_executable):
            return {"error": "Python executable not found in the specified virtual environment."}, 404

        if operation == 'run_script':
            if not script_path:
                return {"error": "The 'scriptPath' parameter is required for running a script."}, 400

            if not os.path.isfile(script_path):
                return {"error": "The specified script file does not exist."}, 404

            try:
                
                with open(script_path, "r") as f:
                    content = f.readlines()

                has_blocking, blocking_calls, _ = detect_blocking_functions("\n".join(content))
                if has_blocking:
                    
                    if not inputs_for_test:
                        return {"error": "The 'inputs_for_test' parameter is required for running a script." + 
                                f'Blocking functions detected: {blocking_calls}, echo -e "first_line\nsecond_line" | python -B your_script.py' }, 400

                    # Run the script, sending the simulated input to stdin
                    result = subprocess.run(
                        [python_executable, "-B", script_path],
                        input=inputs_for_test,  # Send the simulated input
                        capture_output=True,    # Capture stdout and stderr
                        text=True               # Return output as text (not bytes)
                    )
                else:
                    result = subprocess.run(
                        [python_executable, "-B", script_path],
                        capture_output=True,
                        text=True
                    )

                if result.returncode != 0:
                    if "EOFError: EOF when reading a line" in result.stderr.strip():
                        return {"error": 'Item in "inputs_for_test" is not enough'}, 500
                    else:
                        return {"error": result.stderr.strip()}, 500
                else:
                    return {"message": result.stdout.strip()}, 200
                
            except Exception as e:
                return {"error": str(e), "traceback": traceback.format_exc()}, 500
            
        elif operation == 'pip_install':
            if not package_name:
                return {"error": "The 'packageName' parameter is required for pip install."}, 400

            try:
                result = subprocess.run(
                    [python_executable, "-m", "pip", "install", package_name],
                    capture_output=True,
                    text=True
                )
                return {
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip(),
                    "returncode": result.returncode
                }, 200
            except Exception as e:
                return {"error": str(e), "traceback": traceback.format_exc()}, 500

        elif operation == 'pip_uninstall':
            if not package_name:
                return {"error": "The 'packageName' parameter is required for pip uninstall."}, 400

            try:
                result = subprocess.run(
                    [python_executable, "-m", "pip", "uninstall", "-y", package_name],
                    capture_output=True,
                    text=True
                )
                return {
                    "stdout": result.stdout.strip(),
                    "stderr": result.stderr.strip(),
                    "returncode": result.returncode
                }, 200
            except Exception as e:
                return {"error": str(e), "traceback": traceback.format_exc()}, 500

        elif operation == 'check_module':
            if not module_name:
                return {"error": "The 'moduleName' parameter is required to check module existence."}, 400

            try:
                result = subprocess.run(
                    [python_executable, "-c", f"import {module_name}"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return {"message": f"Module '{module_name}' is installed."}, 200
                else:
                    return {"message": f"Module '{module_name}' is not installed."}, 404
            except Exception as e:
                return {"error": str(e), "traceback": traceback.format_exc()}, 500

        elif operation == 'list_modules':
            try:
                result = subprocess.run(
                    [python_executable, "-m", "pip", "list"],
                    capture_output=True,
                    text=True
                )
                return {"modules": result.stdout.strip()}, 200
            except Exception as e:
                return {"error": str(e), "traceback": traceback.format_exc()}, 500

        else:
            return {"error": f"Unsupported operation '{operation}'."}, 400

    except Exception as e:
        return {"error": str(e), "traceback": traceback.format_exc()}, 500
