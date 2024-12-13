def get_folder_operations_spec():
    """OpenAPI specification for folder operations."""
    return {
        "/folder_operations": {
            "get": {
                "operationId": "folderOperations",
                "summary": "Performs basic folder operations (create, delete, rename, move, copy, list).",
                "parameters": [
                    {
                        "name": "operation",
                        "in": "query",
                        "description": (
                            "The operation to perform ('create', 'delete', 'rename', 'move', 'copy', 'list'). "
                            "Required."
                        ),
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "path",
                        "in": "query",
                        "description": "Relative path to the folder. Required.",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "commitMessage",
                        "in": "query",
                        "description": (
                            "Commit message for operations that modify the folder structure "
                            "('create', 'delete', 'rename', 'move', 'copy'). Required for these operations."
                        ),
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "targetPath",
                        "in": "query",
                        "description": (
                            "Target path for renaming, moving, or copying. "
                            "Required for 'rename', 'move', and 'copy' operations."
                        ),
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "recursive",
                        "in": "query",
                        "description": (
                            "Whether to include all contents recursively (for 'delete' and 'list'). Defaults to 'false'."
                        ),
                        "required": False,
                        "schema": {"type": "boolean", "default": False}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Operation completed successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {"type": "string"},
                                        "warning": {"type": "string"},
                                        "commit_sha": {"type": "string"},
                                    },
                                    "required": ["message"]
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Bad request, such as missing or invalid parameters.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"type": "string"}
                                    },
                                    "required": ["error"]
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Folder not found.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"type": "string"}
                                    },
                                    "required": ["error"]
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Internal server error.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {"type": "string"}
                                    },
                                    "required": ["error"]
                                }
                            }
                        }
                    }
                }
            }
        }
    }
