import uuid

from flask import Blueprint, request

from fhir_server import mongo
from fhir_server.core.utils.vars import instant_datetime, get_resource_schema

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/api/v1//patient', methods=['GET'])
def get_patient():

    # TODO: Implement this list of args
    args_list = ["birthdate", "gender",

                 "general_practitioner", "_security", "active", "_filter", "_profile",
                 "phone", "_tag", "organization", "_has", "address_use", "source", "_id", "_text", "_content", "family"]

    search_criteria = {
        "$and": []
    }

    if request.args.get("deceased"):
        or_query = {"$or": [
            {"deceasedBoolean": request.args.get("deceased")},
            {"deceasedDateTime": request.args.get("deceased")}
        ]}

        search_criteria["$and"].append(or_query)

    if request.args.get("death_date"):
        search_criteria["$and"].append({"deceasedDateTime": request.args.get("death_date")})

    if request.args.get("address_state"):
        search_criteria["$and"].append({"address.state": request.args.get("address_state")})

    if request.args.get("address_country"):
        search_criteria["$and"].append({"address.country": request.args.get("address_country")})

    if request.args.get("address_city"):
        search_criteria["$and"].append({"address.city": request.args.get("address_city")})

    if request.args.get("address_postalcode"):
        search_criteria["$and"].append({"address.postalCode": request.args.get("address_postalcode")})

    if request.args.get("address"):
        print("Not implemented yet")  # TODO: Implement this

    if request.args.get("_lastUpdated"):
        search_criteria["$and"].append({"meta.lastUpdated": request.args.get("_lastUpdated")})

    if request.args.get("given"):
        search_criteria["$and"].append({"name.given": request.args.get("given")})

    if request.args.get("link"):
        print("Not implemented yet")  # TODO: Implement this

    if request.args.get("phonetic"):
        print("Not implemented yet")  # TODO: Implement this

    if request.args.get("telecom"):
        print("Not implemented yet")  # TODO: Implement this

    if request.args.get("email"):
        search_criteria["$and"].append({"telecom": {"$elemMatch": {"system": request.args.get("email")}}})

    if request.args.get("identifier"):
        print("Not implemented yet")



    page_number = 1
    page_size = 10

    skip_count = (page_number - 1) * page_size

    for arg in args_list:
        if arg in request.args:
            search_criteria["$and"].append({arg: request.args.get(arg)})

    total_count = mongo["patient"].count_documents(search_criteria)
    complete_url = request.base_url + '?' + request.query_string.decode('utf-8')

    results = mongo["patient"].find(search_criteria).skip(skip_count).limit(page_size)

    adding_search = {
        "fullUrl": "http://localhost:5000/Patient/5ea8b1e4b7a8c1a4c2b9e6b5d6e",
        "resource": {},
        "search": {
            "mode": "match"
        }
    }

    bundle = {
        "resourceType": "Bundle",
        "id": str(uuid.uuid4()),
        "meta": {
            "lastUpdated": instant_datetime()
        },
        "type": "searchset",
        "total": total_count,
        "link": [
            {
                "relation": "self",
                "url": complete_url
            }
        ],
    }

    if total_count == 0:
        return bundle

    return []
