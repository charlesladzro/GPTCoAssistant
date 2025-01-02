def get_git_operations_spec():
    """OpenAPI specification for Git operations."""
    return {
        "/git_operations": {
            "post": {
                "operationId": "gitOperations",
                "summary": "Performs Git operations (init, clone, pull, add, commit, push, branch, checkout, status, log).",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "description": "The Git operation to perform ('clone', 'pull', 'add', 'commit', 'push', 'branch', 'checkout', 'status', 'log')."
                                    },
                                    "repoPath": {
                                        "type": "string",
                                        "description": "Path to the Git repository (required for 'pull', 'add', 'commit', 'push', 'branch', 'checkout', 'status', 'log')."
                                    },
                                    "remoteUrl": {
                                        "type": "string",
                                        "description": "Remote URL for cloning (required for 'clone')."
                                    },
                                    "targetPath": {
                                        "type": "string",
                                        "description": "Target path for cloning (required for 'clone')."
                                    },
                                    "branchName": {
                                        "type": "string",
                                        "description": "Branch name for branch or checkout operations."
                                    },
                                    "commitMessage": {
                                        "type": "string",
                                        "description": "Commit message for 'commit'."
                                    },
                                    "files": {
                                        "type": "string",
                                        "description": "Files to add (space-separated list). Defaults to all files."
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
