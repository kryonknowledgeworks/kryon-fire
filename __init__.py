from flask import Flask, jsonify, request, render_template
from flask_swagger_ui import get_swaggerui_blueprint
import json

import rest_handler

# creating a Flask app
app = Flask(__name__, template_folder='templates')


@app.route('/v1/api/resource/<resource_type>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def endpoint(resource_type):
    if request.method == 'POST':
        resource = rest_handler.add_resource(resource_type, request.json)
        return jsonify(resource)
    else:
        return "Not implemented yet.", 400


@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger.json')
def swagger():
    with open('swagger.json', 'r') as f:
        return jsonify(json.load(f))


# driver function
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
