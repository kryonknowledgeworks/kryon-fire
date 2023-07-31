from core.resources.Patient import Patient
from core.utils.validator import DataTypeValidator


def add_resource(resource_type: str, json):
    if resource_type.lower() == 'patient':
        patient = Patient(json)
        validation_result = DataTypeValidator().validation_report()
        DataTypeValidator().reset_error_details()
        return validation_result
