def get_file_operations_spec():
    """OpenAPI specification for file operations."""
    return {
        "/file_operations": {
            "get": {
                "operationId": "fileOperations",
                "summary": "Performs basic file operations (read, write, delete, rename, move, copy).",
                "parameters": [
                    {
                        "name": "operation",
                        "in": "query",
                        "description": "The operation to perform ('read', 'write', 'delete', 'rename', 'move', 'copy'). Required.",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "path",
                        "in": "query",
                        "description": "Relative path to the file. Required.",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "commitMessage",
                        "in": "query",
                        "description": (
                            "Commit message for operations that modify the file system "
                            "('write', 'delete', 'rename', 'move', 'copy'). Required for these operations."
                        ),
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "content",
                        "in": "query",
                        "description": "Content to write to the file (required for 'write' operation).",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "targetPath",
                        "in": "query",
                        "description": "Target path for renaming, moving, or copying. Required for 'rename', 'move', and 'copy' operations.",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "encoding",
                        "in": "query",
                        "description": "The file encoding. Defaults to 'utf-8'.",
                        "required": False,
                        "schema": {"type": "string", "default": "utf-8"}
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
                        "description": "File not found.",
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
