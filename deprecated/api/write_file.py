def get_write_file_spec():
    """OpenAPI specification for the writeFile action."""
    return {
        "/write_file": {
            "post": {
                "operationId": "writeFile",
                "summary": "Writes content to a specified file.",
                "parameters": [
                    {
                        "name": "path",
                        "in": "query",
                        "description": "Relative path to the file to write. Required.",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "content": {
                                        "description": "Content to write into the file.",
                                        "type": "string"
                                    },
                                    "append": {
                                        "description": "If true, appends to the file; otherwise overwrites. Default is false.",
                                        "type": "boolean",
                                        "default": False
                                    }
                                },
                                "required": ["content"]
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "File written successfully.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "message": {
                                            "type": "string",
                                            "example": "File written successfully."
                                        },
                                        "status": {
                                            "type": "string",
                                            "example": "success"
                                        }
                                    },
                                    "required": ["message", "status"]
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
                                            "type": "string",
                                            "example": "Invalid parameters."
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
                                            "type": "string",
                                            "example": "Internal server error."
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
