import os
import json
from benedict import benedict

global schema

schema_path = os.getcwd() + '/schema/patient.json'

# read file
with open(schema_path, 'r', encoding="utf8") as schema_json:
    data = schema_json.read()

# parse file
obj = json.loads(data)


def get_patient_schema():
    return benedict(obj)


def build_schema_ref_path(resource_ref: str):
    if resource_ref.startswith('#/'):
        return resource_ref[2:].replace('/', '.')
    else:
        return resource_ref
