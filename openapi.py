from flask import jsonify
import yaml
import os
import importlib
from config import SERVER_URL, TITLE, VERSION

def load_openapi_specs():
    """Dynamically load OpenAPI specifications from the api directory."""
    openapi_dir = "api"
    specs = {}
    
    for filename in os.listdir(openapi_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"{openapi_dir.replace('/', '.')}.{filename[:-3]}"
            module = importlib.import_module(module_name)

            spec_name = f"get_{filename[:-3]}_spec"
            if hasattr(module, spec_name):
                spec_func = getattr(module, spec_name)
                specs.update(spec_func())
    
    return specs

def get_openapi_spec():
    """Dynamically generate the OpenAPI specification by combining individual action specs."""
    paths = load_openapi_specs()

    return {
        "openapi": "3.1.0",
        "info": {
            "title": TITLE,
            "version": VERSION
        },
        "servers": [
            {"url": SERVER_URL}
        ],
        "paths": paths
    }

def get_openapi_json_endpoint():
    """Serve OpenAPI spec as JSON."""
    openapi_spec = get_openapi_spec()
    return jsonify(openapi_spec)

def get_openapi_yaml_endpoint():
    """Serve OpenAPI spec as YAML."""
    openapi_spec = get_openapi_spec()
    return yaml.dump(openapi_spec, sort_keys=False), 200, {'Content-Type': 'text/plain'}
