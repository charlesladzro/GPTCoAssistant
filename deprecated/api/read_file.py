def get_read_file_spec():
    """OpenAPI specification for the readFile action."""
    return {
        "/read_file": {
            "get": {
                "operationId": "readFile",
                "summary": "Reads the content of a specified file.",
                "parameters": [
                    {
                        "name": "path",
                        "in": "query",
                        "description": "Relative path to the file to read. Required.",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "encoding",
                        "in": "query",
                        "description": "The file encoding to use for reading. Defaults to 'utf-8'.",
                        "required": False,
                        "schema": {"type": "string", "default": "utf-8"}
                    },
                    {
                        "name": "maxBytes",
                        "in": "query",
                        "description": "Maximum number of bytes to read from the file. If not specified, reads the entire file.",
                        "required": False,
                        "schema": {"type": "integer"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Content of the specified file.",
                        "content": {
                            "text/plain": {"schema": {"type": "string"}}
                        }
                    },
                    "400": {
                        "description": "Bad request, such as missing or invalid parameters.",
                        "content": {
                            "application/json": {"schema": {"type": "object"}}
                        }
                    },
                    "404": {
                        "description": "File not found.",
                        "content": {
                            "application/json": {"schema": {"type": "object"}}
                        }
                    },
                    "500": {
                        "description": "Internal server error.",
                        "content": {
                            "application/json": {"schema": {"type": "object"}}
                        }
                    }
                }
            }
        }
    }
