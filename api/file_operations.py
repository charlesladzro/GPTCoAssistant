def get_file_operations_spec():
    """OpenAPI specification for file operations."""
    return {
        "/file_operations": {
            "post": {
                "operationId": "fileOperations",
                "summary": "Performs basic file operations (read, write, delete, rename, move, copy).",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "description": "The operation to perform ('read', 'write', 'delete', 'rename', 'move', 'copy')."
                                    },
                                    "path": {
                                        "type": "string",
                                        "description": "Relative path to the file."
                                    },
                                    "commitMessage": {
                                        "type": "string",
                                        "description": "Commit message for operations that modify the file system ('write', 'delete', 'rename', 'move', 'copy')."
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "Content to write to the file (required for 'write' operation)."
                                    },
                                    "targetPath": {
                                        "type": "string",
                                        "description": "Target path for renaming, moving, or copying (required for 'rename', 'move', and 'copy' operations)."
                                    },
                                    "encoding": {
                                        "type": "string",
                                        "description": "The file encoding. Defaults to 'utf-8'.",
                                        "default": "utf-8"
                                    },
                                    "assistantLastResponse": {
                                        "type": "string",
                                        "description": "The exact text of the assistant previous response, rather than summarizing or simplifying it (not required for 'GPT_Instructions.md' file reading)."
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
