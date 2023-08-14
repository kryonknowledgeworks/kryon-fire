""" This module is used to handle the REST API requests. """
import uuid
import json

from flask import request, Blueprint

from fhir_server import mongo
from fhir_server.core.resources.Resource_handler import ResourceHandler
from fhir_server.core.utils.vars import generate_random_sequence, instant_datetime
from bson.json_util import dumps

resource_controller_bp = Blueprint('resource_controller', __name__)


@resource_controller_bp.route(rule='/api/v1/resource/<resource_type>', methods=['POST', 'PUT'])
def resource_endpoint(resource_type: str):
    """This function handles the POST, PUT and DELETE requests for a resource type."""
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


@resource_controller_bp.route(rule='/api/v1/resource/<resource_type>', methods=['GET', 'PATCH'])
def resource_endpoint_get(resource_type: str):
    """This function handles the GET requests for a resource type."""
    resource_id = request.args.get('resource_id')
    if resource_id:
        pipeline = [
            {'$match': {'id': resource_id}},
            {'$group': {'_id': None, 'max_version': {'$max': {'$toInt': '$meta.versionId'}}}}
        ]

        max_version_id = list(mongo[resource_type.lower()].aggregate(pipeline))
        if max_version_id:
            max_version_id = max_version_id[0].get('max_version')

            query = {
                '$and': [
                    {'id': resource_id},
                    {'meta.versionId': str(max_version_id)}
                ]
            }

            result = mongo[resource_type.lower()].find_one(query, {"_id": 0})
            if result:
                json_data = dumps(result)
                return json.dumps(json.loads(json_data), indent=2), 200
            else:
                return {"errors": "Resource id not found"}, 404
        else:
            return {"errors": "Resource id not found"}, 404


def add_resource(resource_type: str, resource_json: dict):
    """This function is used to add a resource."""
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
    """This function is used to update a resource."""
    pipeline = [
        {'$match': {'id': resource_id}},
        {'$group': {'_id': None, 'max_version': {'$max': {'$toInt': '$meta.versionId'}}}}
    ]

    max_version_id = list(mongo[resource_type.lower()].aggregate(pipeline))
    if max_version_id:
        max_version_id = max_version_id[0].get('max_version')

        query = {
            '$and': [
                {'id': resource_id},
                {'meta.versionId': str(max_version_id)}
            ]
        }

        result = mongo[resource_type.lower()].find_one(query, {"_id": 0})

        if result:
            json_data = dumps(result)
            resource = json.loads(json_data)
            version_id = str(int(resource.get("meta").get("versionId")) + 1)
            json_details = {
                "id": resource_id,
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
            return {"errors": "Resource id not found"}, 404
    else:
        return {"errors": "Resource id not found"}, 404
