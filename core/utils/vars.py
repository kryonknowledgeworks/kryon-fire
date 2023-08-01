import os
import json
from benedict import benedict


def get_resource_schema(resource_type: str):

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
    if resource_ref.startswith('#/'):
        return resource_ref[2:].replace('/', '.')
    else:
        return resource_ref
