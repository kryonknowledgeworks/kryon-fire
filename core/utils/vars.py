"""This module contains utility functions for variables."""
import os
import json
from benedict import benedict


def get_resource_schema(resource_type: str):
    """Returns a schema for a given resource type."""
    schema_path = os.getcwd() + f'/schema/{resource_type}.json'

    if not os.path.exists(schema_path):
        return None

    # read file
    with open(schema_path, 'r', encoding="utf8") as schema_json:
        data = schema_json.read()

    # parse file
    obj = json.loads(data)

    return benedict(obj)


def build_schema_ref_path(resource_ref: str):
    """Builds a path to a schema reference."""
    if resource_ref.startswith('#/'):
        return resource_ref[2:].replace('/', '.')
    return resource_ref


def change_datatype_valid_format(datatype):
    if datatype == "string":
        return str
    elif datatype == "integer":
        return int
    elif datatype == "boolean":
        return bool
    elif datatype == "float":
        return float
    elif datatype == "array":
        return list
    elif datatype == "object":
        return dict
