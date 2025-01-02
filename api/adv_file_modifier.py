def get_adv_file_modifier_spec():
    """OpenAPI specification for advanced file modification."""
    return {
        "/adv_file_modifier": {
            "post": {
                "operationId": "advFileModifier",
                "summary": "Performs advanced file modification operations. Optimized for efficient processing using incremental updates and chunk-based file handling.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "operation": {
                                        "type": "string",
                                        "description": "The operation to perform ('replace', 'line_replace', 'regex_replace', 'append', 'prepend', 'batch_process')."
                                    },
                                    "path": {
                                        "type": "string",
                                        "description": "Relative path to the file."
                                    },
                                    "commitMessage": {
                                        "type": "string",
                                        "description": "Commit message for operations that modify the file system."
                                    },
                                    "searchStr": {
                                        "type": "string",
                                        "description": "String to search for (required for 'replace', 'append', 'prepend')."
                                    },
                                    "replaceStr": {
                                        "type": "string",
                                        "description": "String to replace the search string with (required for 'replace' and 'regex_replace')."
                                    },
                                    "lineNumber": {
                                        "type": "integer",
                                        "description": "Line number to replace (required for 'line_replace')."
                                    },
                                    "newLine": {
                                        "type": "string",
                                        "description": "New content for the specified line (required for 'line_replace')."
                                    },
                                    "pattern": {
                                        "type": "string",
                                        "description": "Regex pattern to search for (required for 'regex_replace')."
                                    },
                                    "assistantLastResponse": {
                                        "type": "string",
                                        "description": "The exact text of the assistant previous response, rather than summarizing or simplifying it."
                                    }
                                },
                                "required": ["operation", "path", "commitMessage", "assistantLastResponse"]
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
                                        "commit_sha": {"type": "string"}
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