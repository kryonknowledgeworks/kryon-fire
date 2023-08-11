import os
import sys

from flask import Flask
from flask_pymongo import PyMongo

# creating a Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

with app.app_context():
    env_config = {
        "development": "fhir_server.configuration.env_config.DevConfig",
    }

    config_class = env_config.get(os.getenv("FLASK_ENV"))
    if not config_class:
        print("Invalid FLASK_ENV environment variable entry. ", file=sys.stderr)
        sys.exit(1)

    app.config.from_object(config_class)

    # Initialize MongoDB
    mongo = PyMongo(app).db

    # Importing routes
    from fhir_server.api.index import index_controller_bp
    from fhir_server.api.rest_handler import resource_controller_bp

    # Registering blueprints
    app.register_blueprint(index_controller_bp)
    app.register_blueprint(resource_controller_bp)
