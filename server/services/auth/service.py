import os

from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from server.db import db
from server.api import api
from server.utils.jwt import jwt_manager
from server.utils.initialize.user_service import initialize_user_database  # noqa
from server.core.models.db_models import (user)  # noqa - import all models for table initfrom server.api import api
from server.services.heathcheck.apis.heathcheck import ns as ns_heathcheck
from server.services.auth.apis.auth import ns as ns_auth
from server.services.auth.apis.user import ns as ns_user
from server.logger import logger


load_dotenv()


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(
        os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS"))
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        minutes=int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_MINUTES")))


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

    is_debug = os.environ.get("DEBUG", False)

    with app.app_context():
        if is_debug:
            db.drop_all()

        # TODO: Add DB-Migrations!
        logger.info("-------------- CREATE TABLES --------------")
        db.create_all()

        initialize_user_database(app)

    return app
