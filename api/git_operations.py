def get_git_operations_spec():
    """OpenAPI specification for Git operations."""
    return {
        "/git_operations": {
            "get": {
                "operationId": "gitOperations",
                "summary": "Performs Git operations (init, clone, pull, add, commit, push, branch, checkout, status, log).",
                "parameters": [
                    {
                        "name": "operation",
                        "in": "query",
                        "description": "The Git operation to perform ('clone', 'pull', 'add', 'commit', 'push', 'branch', 'checkout', 'status', 'log'). Required.",
                        "required": True,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "repoPath",
                        "in": "query",
                        "description": "Path to the Git repository (required for 'pull', 'add', 'commit', 'push', 'branch', 'checkout', 'status', 'log').",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "remoteUrl",
                        "in": "query",
                        "description": "Remote URL for cloning. Required for 'clone'.",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "targetPath",
                        "in": "query",
                        "description": "Target path for cloning. Required for 'clone'.",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "branchName",
                        "in": "query",
                        "description": "Branch name for branch or checkout operations.",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "commitMessage",
                        "in": "query",
                        "description": "Commit message for 'commit'.",
                        "required": False,
                        "schema": {"type": "string"}
                    },
                    {
                        "name": "files",
                        "in": "query",
                        "description": "Files to add (space-separated list). Defaults to all files.",
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
                                        "message": {
                                            "type": "string"
                                        }
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
                    "500": {
                        "description": "Internal server error.",
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
                    }
                }
            }
        }
    }
