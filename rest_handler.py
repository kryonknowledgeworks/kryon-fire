""" This module is used to handle the REST API requests. """
from core.resources.Resource_handler import ResourceHandler


def add_resource(resource_type: str, json):
    resource_handler = ResourceHandler(json, resource_type.lower())
    validation_result = resource_handler.validation_result()
    return validation_result
