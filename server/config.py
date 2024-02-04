from datetime import timedelta

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


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = "mysql://serviceuser:devpassword@127.0.0.1:3307/weeklychef"  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "f1ppweq9b3234935d89426aas6303uu38865c1a12574ac9deb393dp34bc8f21eb9920124"  # noqa
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)  # timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


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
