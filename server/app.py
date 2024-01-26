"""
General Flask-App creation for monoith architecture
"""
from datetime import timedelta

from flask import Flask

from db import db
from api import api
from services.auth.jwt import jwt_manager
# from utils.initialize import initialize_database


class FlaskConfig:
    SQLALCHEMY_DATABASE_URI = "mysql://serviceuser:devpassword@127.0.0.1:3307/weeklychef"  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "f1ae9b76935d89426cec6993698e865c1a12574ac9deb393dcdbc8f21eb76998"  # noqa
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


def create_app() -> Flask:
    # Create app and configuration
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)

    # init app
    db.init_app(app)
    api.init_app(app)
    jwt_manager.init_app(app)

    # add errorhandler
    @app.errorhandler(500)
    def internal_server_error(error):
        err_msg = error if app.debug else "Unexpected internal error."
        return {"error": err_msg}, 500

    # initialize db tables
    with app.app_context():
        db.create_all()

    # initialize db with starting data
    # initialize_database(app=app)

    return app
