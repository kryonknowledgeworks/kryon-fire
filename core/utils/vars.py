import os

global schema

import json

schema_path = os.getcwd() + '/schema/patient.json'
from benedict import benedict

# read file
with open(schema_path, 'r', encoding="utf8") as myfile:
    data = myfile.read()

# parse file
obj = json.loads(data)
print("###################################3")


def get_patient_schema():
    return benedict(obj)


def build_schema_ref_path(resource_ref: str):
    if resource_ref.startswith('#/'):
        return resource_ref[2:].replace('/', '.')
    else:
        return resource_ref
