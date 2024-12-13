from flask import request
import os
from func_utils import resolve_path

def write_file_action():
    """Action handler for the /writeFile endpoint."""

    # Extraire les données du corps de la requête JSON
    path = request.args.get('path')  # Le chemin est désormais dans les paramètres de requête
    request_data = request.json
    content = request_data.get('content', '')
    append = request_data.get('append', False)

    if not path:
        return {"error": "The 'path' parameter is required."}, 400

    try:
        # Résoudre le chemin du fichier
        resolved_path = resolve_path(path)
        mode = 'a' if append else 'w'

        # Écrire le contenu dans le fichier
        with open(resolved_path, mode, encoding='utf-8') as file:
            file.write(content)

        # Réponse en cas de succès
        return {
            "status": "success",
            "message": f"File written successfully at {resolved_path}."
        }, 200

    except FileNotFoundError:
        # Gestion du cas où le chemin est invalide
        return {
            "status": "error",
            "message": f"File not found or invalid path: {path}."
        }, 400

    except (IOError, OSError) as e:
        # Gestion des erreurs système
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }, 500
