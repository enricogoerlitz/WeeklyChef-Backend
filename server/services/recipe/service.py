import os

from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from server.db import db
from server.api import api
from server.utils.jwt import jwt_manager
from server.utils.initialize.recipe_service import initialize_dummy_database  # noqa
from server.core.models.db_models import (cart, recipe, planner, supermarket)  # noqa - import all models for table initfrom server.api import api
from server.services.heathcheck.apis.heathcheck import ns as ns_heathcheck
from server.services.recipe.apis.recipe import ns as ns_recipe
from server.services.recipe.apis.ingredient import ns as ns_ingredient
from server.services.recipe.apis.category import ns as ns_category
from server.services.recipe.apis.unit import ns as ns_unit
from server.services.recipe.apis.tag import ns as ns_tag
from server.services.recipe.apis.collection import ns as ns_collection
from server.services.recipe.apis.supermarket import ns as ns_supermarket
from server.services.recipe.apis.planner import ns as ns_planner
from server.services.recipe.apis.cart import ns as ns_cart
from server.logger import logger


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
    api.add_namespace(ns_recipe)
    api.add_namespace(ns_ingredient)
    api.add_namespace(ns_collection)
    api.add_namespace(ns_category)
    api.add_namespace(ns_unit)
    api.add_namespace(ns_tag)
    api.add_namespace(ns_supermarket)
    api.add_namespace(ns_planner)
    api.add_namespace(ns_cart)

    is_debug = os.environ.get("DEBUG", False)

    with app.app_context():
        if is_debug:
            db.drop_all()

        # TODO: Add DB Migrations!
        logger.info("-------------- CREATE TABLES --------------")
        db.create_all()

        if is_debug:
            # initialize db with starting data
            # initialize_dummy_database(app)
            pass

    return app
