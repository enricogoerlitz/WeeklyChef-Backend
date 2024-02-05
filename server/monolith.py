import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from server.db import db
from server.api import api
from server.utils.jwt import jwt_manager
from server.utils.initialize import initialize_database
from server.core.models.db_models import *  # noqa - import all models for table initfrom server.api import api
from server.services.heathcheck.apis.heathcheck import ns as ns_heathcheck
from server.services.auth.apis.auth import ns as ns_auth
from server.services.auth.apis.user import ns as ns_user
from server.services.recipe.apis.recipe import ns as ns_recipe
from server.services.recipe.apis.ingredient import ns as ns_ingredient
from server.services.recipe.apis.category import ns as ns_category
from server.services.recipe.apis.unit import ns as ns_unit
from server.services.recipe.apis.tag import ns as ns_tag
from server.services.recipe.apis.collection import ns as ns_collection


load_dotenv()


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")  # noqa
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES")))  # noqa
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_MINUTES")))  # noqa


def create_app(database_uri: str = None) -> Flask:
    # Create app and configuration
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    if database_uri is not None:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    # init app
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    jwt_manager.init_app(app)

    # add namespaces
    api.add_namespace(ns_heathcheck)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_user)
    api.add_namespace(ns_recipe)
    api.add_namespace(ns_ingredient)
    api.add_namespace(ns_collection)
    api.add_namespace(ns_category)
    api.add_namespace(ns_unit)
    api.add_namespace(ns_tag)

    # add errorhandler
    @app.errorhandler(500)
    def internal_server_error(error):
        err_msg = error if app.debug else "Unexpected internal error."
        return {"error": err_msg}, 500

    # initialize db tables
    with app.app_context():
        db.drop_all()
        db.create_all()

    # initialize db with starting data
    initialize_database(app=app)

    return app
