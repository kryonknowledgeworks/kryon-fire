""" This module is used to handle the REST API requests. """
import uuid
import json

from flask import request, Blueprint, jsonify

from fhir_server import mongo
from fhir_server.core.resources.Resource_handler import ResourceHandler
from fhir_server.core.utils.vars import generate_random_sequence, instant_datetime
from bson.json_util import dumps

resource_controller_bp = Blueprint('resource_controller', __name__)


@resource_controller_bp.route(rule='/api/v1/resource/<resource_type>', methods=['POST', 'PUT', 'DELETE'])
def resource_endpoint(resource_type: str):
    if request.method == 'POST':
        resource, statuscode = add_resource(resource_type, request.json)
        return resource, statuscode

    elif request.method == 'PUT':
        resource_id = request.args.get('resource_id')
        if resource_id:
            resource, statuscode = update_resource(resource_type, request.json, resource_id)
            return resource, statuscode
        else:
            return {"errors": "Resource id not found"}, 404
    else:
        return {"errors": "Not implemented yet."}, 400


@resource_controller_bp.route(rule='/api/v1/resource/<resource_type>', methods=['GET'])
def resource_endpoint_get(resource_type: str):
    resource_id = request.args.get('resource_id')
    if resource_id:
        resource = mongo[resource_type.lower()].find({"id": resource_id}, {"_id": 0})
        print(dumps(resource))
        if resource:
            return resource
        else:
            return jsonify({"message": "Document not found."}), 404

        # resource = mongo[resource_type.lower()].find_one({"id": resource_id}, {"_id": 0})
        # if resource:
        #     json_data = dumps(resource)
        #     return json.dumps(json.loads(json_data), indent=2), 200
        # else:
        #     return {"errors": "Resource id not found"}, 400


def add_resource(resource_type: str, resource_json: dict):
    resource_handler = ResourceHandler(resource_json, resource_type.lower())
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

        json_details = {
            "id": str(uuid.uuid4()),
            "meta": {
                "versionId": "1",
                "lastUpdated": instant_datetime(),
                "source": f"#{generate_random_sequence()}"
            },
            "text": {
                "status": "generated",
            }}

        resource_json.update(json_details)
        mongo[resource_type.lower()].insert_one(resource_json)
        return json_details, 201


def update_resource(resource_type, resource_json, resource_id):
    resource = mongo[resource_type.lower()].find_one({"id": resource_id}, {"_id": 0})
    if resource:
        version_id = str(int(resource.meta.versionId) + 1)
        json_details = {
            "meta": {
                "versionId": version_id,
                "lastUpdated": instant_datetime(),
                "source": f"#{generate_random_sequence()}"
            },
            "text": {
                "status": "updated",
            }
        }

        resource_json.update(json_details)
        mongo[resource_type.lower()].insert_one(resource_json)
        return json_details, 200
    else:
        return {"errors": "Resource id not found"}, 400
