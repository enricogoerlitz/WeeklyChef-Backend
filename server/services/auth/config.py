
import os
from datetime import timedelta

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv


from db import db
from api import api
from utils.jwt import jwt_manager
from core.models.db_models import *  # noqa - import all models for table initfrom api import api
from services.heathcheck.apis.heathcheck import ns as ns_heathcheck
from services.auth.apis.auth import ns as ns_auth
from services.auth.apis.user import ns as ns_user


load_dotenv()


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")                   # noqa
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES"))    # noqa
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_MINUTES"))   # noqa


def create_app(
        database_uri: str = None,
        jwt_access_token_expires_in_minutes: int = None
) -> Flask:
    # Create app and configuration
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    if database_uri is not None:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    if jwt_access_token_expires_in_minutes is not None:
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = jwt_access_token_expires_in_minutes  # noqa

    # init app
    CORS(app)
    db.init_app(app)
    api.init_app(app)
    jwt_manager.init_app(app)

    # add namespaces
    api.add_namespace(ns_heathcheck)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_user)

    # add errorhandler
    @app.errorhandler(500)
    def internal_server_error(error):
        err_msg = error if app.debug else "Unexpected internal error."
        return {"error": err_msg}, 500

    return app
