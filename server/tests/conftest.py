import pytest

from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from config import create_app
from db import db
from core.models.db_models import Role, User
from core.enums import roles


# how to run tests (https://www.youtube.com/watch?v=RLKW7ZMJOf4&ab_channel=PrettyPrinted):  # noqa
#   cd ./server
#   python -m pytest tests/ -W ignore::DeprecationWarning


ADMIN_USERNAME = "AdminUser"
STAFF_USERNAME = "StaffUser"
STANDARD_USERNAME = "StdUser"


@pytest.fixture()
def app():
    app = create_app(database_uri="sqlite://")
    with app.app_context():
        db.drop_all()
        db.create_all()

        std_role = Role(name=roles.STANDARD)
        staff_role = Role(name=roles.STAFF)
        admin_role = Role(name=roles.ADMIN)

        db.session.add_all([std_role, staff_role, admin_role])

        std_user = User(
            username=STANDARD_USERNAME,
            email="std.test@email.com",
            password="password"
        )
        staff_user = User(
            username=STAFF_USERNAME,
            email="staff.test@email.com",
            password="password"
        )
        admin_user = User(
            username=ADMIN_USERNAME,
            email="admin.test@email.com",
            password="password"
        )

        std_user.roles.extend([std_role])
        staff_user.roles.extend([std_role, staff_role])
        admin_user.roles.extend([std_role, staff_role, admin_role])

        db.session.add_all([std_user, staff_user, admin_user])

        db.session.commit()

    yield app


@pytest.fixture()
def client(app: Flask):
    client: FlaskClient = app.test_client()
    return client


@pytest.fixture()
def admin_headers(app: Flask):
    with app.app_context():
        user = User.query.filter_by(username=ADMIN_USERNAME).first()
        access_token = create_access_token(identity=user.to_identity())
        headers = {"Authorization": f"Bearer {access_token}"}

    return headers


@pytest.fixture()
def staff_headers(app: Flask):
    with app.app_context():
        user = User.query.filter_by(username=STAFF_USERNAME).first()
        access_token = create_access_token(identity=user.to_identity())
        headers = {"Authorization": f"Bearer {access_token}"}

    return headers


@pytest.fixture()
def std_headers(app: Flask):
    with app.app_context():
        user = User.query.filter_by(username=STANDARD_USERNAME).first()
        access_token = create_access_token(identity=user.to_identity())
        headers = {"Authorization": f"Bearer {access_token}"}

    return headers
