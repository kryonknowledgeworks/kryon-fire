from core.resources.Organization import Organization
from core.resources.Patient import Patient
from core.resources.Practitioner import Practitioner


def add_resource(resource_type: str, json):
    if resource_type.lower() == 'patient':
        patient = Patient(json)
        validation_result = patient.validation_result()
        return validation_result

    elif resource_type.lower() == 'practitioner':
        practitioner = Practitioner(json)
        validation_result = practitioner.validation_result()
        return validation_result

    elif resource_type.lower() == 'organization':
        organization = Organization(json)
        validation_result = organization.validation_result()
        return validation_result


