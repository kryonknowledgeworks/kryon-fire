""" This module is used to handle the REST API requests. """
import uuid

from flask import request, Blueprint
from datetime import datetime, timezone

from fhir_server import mongo
from fhir_server.core.resources.Resource_handler import ResourceHandler
from fhir_server.core.utils.vars import generate_random_sequence

resource_controller_bp = Blueprint('resource_controller', __name__)


@resource_controller_bp.route('/api/v1/resource/<resource_type>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def resource_endpoint(resource_type: str):
    if request.method == 'POST':
        resource, statuscode = add_resource(resource_type, request.json)
        return resource, statuscode
    else:
        return {"errors": "Not implemented yet."}, 400


def add_resource(resource_type: str, json: dict):
    resource_handler = ResourceHandler(json, resource_type.lower())
    validation_result = resource_handler.validation_result()
    if validation_result:
        json_details = {
            "text": {
                "status": "Validation failed",
                "errors": validation_result
            }
        }

        return json_details, 400

    else:
        formatted_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        formatted_time = formatted_time[:-2] + ':' + formatted_time[-2:]

        json_details = {
            "id": str(uuid.uuid4()),
            "meta": {
                "versionId": "1",
                "lastUpdated": formatted_time,
                "source": f"#{generate_random_sequence()}"
            },
            "text": {
                "status": "generated",
            }}

        json.update(json_details)
        mongo[resource_type.lower()].insert_one(json)
        return json_details, 200
