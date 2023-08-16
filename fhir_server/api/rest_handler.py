""" This module is used to handle the REST API requests."""
import uuid
import json

from flask import request, Blueprint
from bson.json_util import dumps

from fhir_server import mongo
from fhir_server.core.resources.Resource_handler import ResourceHandler
from fhir_server.core.utils.vars import generate_random_sequence, instant_datetime

resource_controller_bp = Blueprint('resource_controller', __name__)

resource_id_missing = {"errors": "Resource id not found"}, 404
not_implemented = {"errors": "Not implemented yet."}, 400


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
            return resource_id_missing

    else:
        return not_implemented


@resource_controller_bp.route(rule='/api/v1/resource/<resource_type>', methods=['GET', 'PATCH',
                                                                                'DELETE'])
def resource_endpoint_get(resource_type: str):
    """This function handles the GET requests for a resource type."""
    if request.method == 'GET':
        resource_id = request.args.get('resource_id')
        if resource_id:
            resource, statuscode = get_resource(resource_id, resource_type)
            return resource, statuscode
        else:
            return resource_id_missing

    elif request.method == 'DELETE':
        resource_id = request.args.get('resource_id')
        if resource_id:
            resource, statuscode = delete_resource(resource_id, resource_type)
            return resource, statuscode
        else:
            return resource_id_missing
    else:
        return not_implemented


def add_resource(resource_type: str, resource_json: dict):
    """This function is used to add a resource."""
    resource_handler = ResourceHandler(resource_json, resource_type.lower())
    validation_result = resource_handler.validation_result()

    if validation_result:
        json_details = {
            "resourceType": "OperationOutcome",
            "text": {
                "status": "generated"
            },
            "issue": [
                {
                    "severity": "error",
                    "code": "processing",
                    "diagnostics": f"Failed to parse request body as JSON resource. Error was: "
                                   f"Invalid JSON content detected.",
                    "errors": validation_result
                }
            ]
        }

        return json_details, 400

    else:
        resource_id = str(uuid.uuid4())
        json_details = {
            "id": resource_id,
            "meta": {
                "versionId": "1",
                "lastUpdated": instant_datetime(),
                "source": f"#{generate_random_sequence()}"
            },
            "text": {
                "status": "generated",
            }
        }

        history_json = {
            "request": {
                "method": "POST",
                "url": f"{resource_type.upper()}/{resource_id}/_history/1"
            },
            "response": {
                "status": "201 Created",
                "etag": "W/\"1\""
            }}

        resource_json.update(json_details)
        resource_json.update(history_json)
        mongo[resource_type.lower()].insert_one(resource_json)

        return json_details, 201


def update_resource(resource_type, resource_json, resource_id):
    """This function is used to update a resource."""
    resource_handler = ResourceHandler(resource_json, resource_type.lower())
    validation_result = resource_handler.validation_result()
    if validation_result:
        json_details = {
            "resourceType": "OperationOutcome",
            "text": {
                "status": "generated"
            },
            "issue": [
                {
                    "severity": "error",
                    "code": "processing",
                    "diagnostics": f"Failed to parse request body as JSON resource. Error was: "
                                   f"Invalid JSON content detected, {validation_result}"
                }
            ]
        }

        return json_details, 400

    else:
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
                        "status": "updated"
                    }
                }

                resource_json.update(json_details)
                mongo[resource_type.lower()].insert_one(resource_json)

                return json_details, 200

            else:
                return resource_id_missing
        else:
            return resource_id_missing


def get_resource(resource_id, resource_type):
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

        result = mongo[resource_type.lower()].find_one(query, {"_id": 0, "request": 0, "response": 0})
        if result:
            json_data = dumps(result)
            json_data = json.loads(json_data)
            if json_data.get("deleted"):
                json_details = {
                    "resourceType": "OperationOutcome",
                    "text": {
                        "status": "generated",
                    },
                    "issue": [
                        {
                            "severity": "error",
                            "code": "processing",
                            "diagnostics": f"Resource was deleted at {json_data.get('meta').get('lastUpdated')}"
                        }
                    ]
                }
                return json.dumps(json_details, indent=2), 400
            else:
                return json.dumps(json_data, indent=2), 200

        else:
            return resource_id_missing

    else:
        return resource_id_missing


def delete_resource(resource_id, resource_type):
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
        result = json.loads(dumps(result))
        if result:
            if result.get("deleted"):
                json_details = {
                    "resourceType": "OperationOutcome",
                    "text": {
                        "status": "generated",
                    },
                    "issue": [
                        {
                            "severity": "information",
                            "code": "informational",
                            "details": {
                                "coding": [
                                    {
                                        "system": "<not implemented.>",
                                        "code": "SUCCESSFUL_DELETE_ALREADY_DELETED",
                                        "display": "Delete succeeded: Resource was already deleted so no action was "
                                                   "taken."
                                    }
                                ]
                            },
                            "diagnostics": f"Not deleted, resource {resource_type.capitalize()}/{resource_id}"
                                           f"/_history/{result.get('meta').get('versionId')} was already deleted."
                        }
                    ]
                }
                return json.dumps(json_details, indent=2), 400
            else:
                json_details = {
                    "deleted": {
                        "resourceType": "OperationOutcome",
                        "text": {
                            "status": "generated",
                        },
                        "issue": [
                            {
                                "severity": "information",
                                "code": "informational",
                                "details": {
                                    "coding": [
                                        {
                                            "system": "<not implemented.>",
                                            "code": "SUCCESSFUL_DELETE",
                                            "display": "Delete succeeded."
                                        }
                                    ]
                                },
                                "diagnostics": "Successfully deleted 1 resource(s). Took 20ms."
                            }
                        ]
                    },
                    "meta": {
                        "versionId": result.get("meta").get("versionId"),
                        "lastUpdated": instant_datetime(),
                        "source": result.get("meta").get("source")
                    }
                }

                mongo[resource_type.lower()].update_one(query, {"$set": json_details})
                return json.dumps(json_details["deleted"], indent=2), 200
        else:
            return resource_id_missing

    else:
        return resource_id_missing
