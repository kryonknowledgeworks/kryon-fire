""" This module is used to handle the REST API requests. """
import uuid
import json

from flask import request, Blueprint
from datetime import datetime, timezone

from fhir_server import mongo
from fhir_server.core.resources.Resource_handler import ResourceHandler
from fhir_server.core.utils.vars import generate_random_sequence
from bson.json_util import dumps

resource_controller_bp = Blueprint('resource_controller', __name__)


@resource_controller_bp.route(rule='/api/v1/resource/create/<resource_type>', methods=['POST', 'PUT', 'DELETE'])
def resource_endpoint(resource_type: str):
    if request.method == 'POST':
        resource, statuscode = add_resource(resource_type, request.json)
        return resource, statuscode
    else:
        return {"errors": "Not implemented yet."}, 400


@resource_controller_bp.route(rule='/api/v1/resource/read/<resource_type>', methods=['GET'])
def resource_endpoint_get(resource_type: str):
    resource_id = request.args.get('resource_id')
    if resource_id:
        resource = mongo[resource_type.lower()].find_one({"id": resource_id}, {"_id": 0})
        if resource:
            json_data = dumps(resource)
            return json.dumps(json.loads(json_data), indent=2), 200
        else:
            return {"errors": "Resource not found"}, 404


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
