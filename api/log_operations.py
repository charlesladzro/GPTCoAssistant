def get_log_operations_spec():
    """OpenAPI specification for log operations."""
    return {
        "/log_operations": {
            "post": {
                "operationId": "logOperations",
                "summary": "Retrieve logs of requests and responses.",
                "requestBody": {
                    "required": False,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "date": {
                                        "type": "string",
                                        "description": "Filter logs by date (YYYY-MM-DD format)."
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Logs retrieved successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "logs": {
                                            "type": "array",
                                            "items": {"type": "object"}
                                        }
                                    },
                                    "required": ["logs"]
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
