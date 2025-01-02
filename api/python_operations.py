def get_python_operations_spec():
    """OpenAPI specification (https://spec.openapis.org/oas/v3.1.0.html) for Python operations."""
    return {
        "/python_operations": {
            "post": {
                "operationId": "pythonOperations",
                "summary": "Performs Python operations in a virtual environment.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "description": "The operation to perform. Supported operations: 'create_venv', 'run_script', 'pip_install', 'pip_uninstall', 'check_module', 'list_modules'."
                                    },
                                    "inputs_for_test": {
                                        "type": "string",
                                        "description": "The inputs for test like 'first_line\\nsecond_line'. Required for 'run_script' if script contains the Python function input()."
                                    },
                                    "commitMessage": {
                                        "type": "string",
                                        "description": "Commit message for operations that modify the file system ('create_venv')."
                                    },
                                    "scriptPath": {
                                        "type": "string",
                                        "description": "Path to the Python script to execute. Required for 'run_script'."
                                    },
                                    "packageName": {
                                        "type": "string",
                                        "description": "Name of the package to install or uninstall. Required for 'pip_install' and 'pip_uninstall'."
                                    },
                                    "moduleName": {
                                        "type": "string",
                                        "description": "Name of the module to check. Required for 'check_module'."
                                    },
                                    "assistantLastResponse": {
                                        "type": "string",
                                        "description": "The exact text of the assistant previous response, rather than summarizing or simplifying it."
                                    }
                                },
                                "required": ["operation", "assistantLastResponse"]
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
                                        "error": {
                                            "type": "string"
                                        }
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
                                        "error": {
                                            "type": "string"
                                        }
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
                                        "error": {
                                            "type": "string"
                                        },
                                        "traceback": {
                                            "type": "string"
                                        }
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
