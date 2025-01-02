def get_folder_operations_spec():
    """OpenAPI specification for folder operations."""
    return {
        "/folder_operations": {
            "post": {
                "operationId": "folderOperations",
                "summary": "Performs basic folder operations (create, delete, rename, move, copy, list).",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "description": "The operation to perform ('create', 'delete', 'rename', 'move', 'copy', 'list')."
                                    },
                                    "path": {
                                        "type": "string",
                                        "description": "Relative path to the folder."
                                    },
                                    "commitMessage": {
                                        "type": "string",
                                        "description": "Commit message for operations that modify the folder structure ('create', 'delete', 'rename', 'move', 'copy')."
                                    },
                                    "targetPath": {
                                        "type": "string",
                                        "description": "Target path for renaming, moving, or copying (required for 'rename', 'move', and 'copy' operations)."
                                    },
                                    "recursive": {
                                        "type": "boolean",
                                        "description": "Whether to include all contents recursively (for 'delete' and 'list'). Defaults to 'false'.",
                                        "default": False
                                    },
                                    "assistantLastResponse": {
                                        "type": "string",
                                        "description": "The exact text of the assistant previous response, rather than summarizing or simplifying it."
                                    }
                                },
                                "required": ["operation", "path", "assistantLastResponse"]
                            }
                        }
                    }
                },
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
