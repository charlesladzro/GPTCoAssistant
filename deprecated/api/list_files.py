def get_list_files_spec():
    """OpenAPI specification for the listFiles action."""
    return {
        "/list_files": {
            "get": {
                "operationId": "listFiles",
                "summary": "Recursively lists files in a directory. Optionally filters by filename and content.",
                "parameters": [
                    {
                        "name": "path",
                        "in": "query",
                        "description": "relative path to directory to list. default is the root directory = '.'",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "recursive",
                        "in": "query",
                        "description": "if true (default) lists files recursively, else only in that directory.",
                        "required": False,
                        "schema": {"type": "boolean", "default": True}
                    },
                    {
                        "name": "filePathRegex",
                        "in": "query",
                        "description": "regex to filter file paths - use for search by file name",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "grepRegex",
                        "in": "query",
                        "description": "an optional regex that lists only files that contain a line matching this pattern",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "listDirectories",
                        "in": "query",
                        "description": "if true, lists directories instead of files",
                        "required": False,
                        "schema": {"type": "boolean"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "List of relative paths of the files",
                        "content": {
                            "text/plain": {"schema": {"type": "string"}}
                        }
                    }
                }
            }
        }
    }
