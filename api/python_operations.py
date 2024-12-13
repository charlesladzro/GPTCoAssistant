def get_python_operations_spec():
    """OpenAPI specification for Python operations."""
    return {
        "/python_operations": {
            "get": {
                "operationId": "pythonOperations",
                "summary": "Performs Python operations in a virtual environment.",
                "parameters": [
                    {
                        "name": "operation",
                        "in": "query",
                        "description": (
                            "The operation to perform. Supported operations: "
                            "'create_venv', 'run_script', 'pip_install', 'pip_uninstall', "
                            "'check_module', 'list_modules'."
                        ),
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "inputs_for_test",
                        "in": "query",
                        "description": (
                            "The inputs for test like 'first_line\\nsecond_line' "
                            "Required for 'run_script' if script contains the python function input()."
                        ),
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "commitMessage",
                        "in": "query",
                        "description": (
                            "Commit message for operations that modify the file system "
                            "('create_venv'). Required for these operations."
                        ),
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "scriptPath",
                        "in": "query",
                        "description": "Path to the Python script to execute. Required for 'run_script'.",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "packageName",
                        "in": "query",
                        "description": "Name of the package to install or uninstall. Required for 'pip_install' and 'pip_uninstall'.",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "moduleName",
                        "in": "query",
                        "description": "Name of the module to check. Required for 'check_module'.",
                        "required": False,
                        "schema": {"type": "string"}
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
