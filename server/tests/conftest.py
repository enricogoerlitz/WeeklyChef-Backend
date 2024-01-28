import pytest

from flask import Flask

from config import create_app
from db import db


# how to run tests (https://www.youtube.com/watch?v=RLKW7ZMJOf4&ab_channel=PrettyPrinted):  # noqa
#   cd ./server
#   python -m pytest tests/ -W ignore::DeprecationWarning


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite://")
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app: Flask):
    return app.test_client()
