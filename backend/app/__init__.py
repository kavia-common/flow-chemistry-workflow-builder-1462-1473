from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
import os
from .routes.health import blp as health_blp

# Database/init imports
from .db import init_db
from .routes.experiments import blp as experiments_blp
from .routes.steps import blp as steps_blp

app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS: allow frontend origin if provided
frontend_origin = os.getenv("FRONTEND_ORIGIN", "*")
CORS(app, resources={r"/*": {"origins": frontend_origin}})

# OpenAPI / Swagger configuration
app.config["API_TITLE"] = "Flow Chemistry Backend API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# Initialize DB (reads env or database/db_connection.txt)
init_db(app)

# Register blueprints
api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(experiments_blp)
api.register_blueprint(steps_blp)
