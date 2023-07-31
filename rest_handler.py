from core.resources.Patient import Patient


def add_resource(resource_type: str, json):
    if resource_type.lower() == 'patient':
        patient = Patient(json)
    print(resource_type)
    print(json)
    return json
