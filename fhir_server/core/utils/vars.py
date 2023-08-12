"""This module contains utility functions for variables."""
import os
import json
import random
import string

from datetime import datetime, timezone
from benedict import benedict


def get_resource_schema(resource_type: str):
    """Returns a schema for a given resource type."""
    schema_path = f'fhir_server/schema/{resource_type}.json'
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


# Generate a random sequence of letters and digits including all alphabets and digits
def generate_random_sequence():
    characters = string.ascii_letters + string.digits
    random_sequence = ''.join(random.choice(characters) for _ in range(16))
    return random_sequence


def instant_datetime():
    """Returns the current time in FHIR format."""
    formatted_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
    formatted_time = formatted_time[:-2] + ':' + formatted_time[-2:]
    return formatted_time
