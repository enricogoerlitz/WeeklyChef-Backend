import pytest

from config import create_app
from db import db


# how to run tests:
#   cd ./server
#   python -m pytest tests/ -W ignore::DeprecationWarning


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite://")
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
