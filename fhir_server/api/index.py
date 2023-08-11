import json

from flask import Blueprint, jsonify, render_template
from flask_swagger_ui import get_swaggerui_blueprint

index_controller_bp = Blueprint('index_controller', __name__)


@index_controller_bp.route('/index.html', methods=['GET'])
@index_controller_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Configure Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "KryonFire Server"
    }
)
index_controller_bp.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


@index_controller_bp.route('/swagger.json')
def swagger():
    with open('static/swagger.json', 'r') as f:
        return jsonify(json.load(f))
