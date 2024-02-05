from flask import Flask
from flask_jwt_extended.utils import decode_token

from server.db import db
from server.services.auth.controller import auth_controller
from server.core.models.db_models import User
from server.core.enums import roles


def create_user(
        username: str = "TestUsername",
        email: str = "test@email.com",
        password: str = "password"
):
    user = User(
        username=username,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    return user


def test_handle_register(app: Flask):
    with app.app_context():
        # given
        data = {
            "username": "TestUsername",
            "email": "test@email.com",
            "password": "password"
        }

        # when
        result_data, status_code = auth_controller.handle_register(data)
        result_user_data = decode_token(result_data["access_token"]).get("sub")
        del result_user_data["id"]

        expected_user_data = {
            **data,
            "roles": [roles.STANDARD]
        }
        del expected_user_data["password"]

        # then
        assert status_code == 200
        assert result_data is not None
        assert "access_token" in result_data
        assert "refresh_token" in result_data
        assert result_user_data == expected_user_data
        assert len(result_data["refresh_token"]) > 10


def test_handle_register_missing_data(app: Flask):
    with app.app_context():
        # given
        data_missing_username = {
            "email": "test@email.com",
            "password": "password"
        }

        data_missing_email = {
            "username": "TestUsername",
            "password": "password"
        }

        data_missing_password = {
            "username": "TestUsername",
            "email": "test@email.com"
        }

        # when
        (result_data_missing_username,
         status_code_missing_username) = auth_controller.handle_register(
            data_missing_username)

        (result_data_missing_email,
         status_code_missing_email) = auth_controller.handle_register(
            data_missing_email)

        (result_data_missing_password,
         status_code_missing_password) = auth_controller.handle_register(
            data_missing_password)

        # then
        assert status_code_missing_username == 400
        assert status_code_missing_email == 400
        assert status_code_missing_password == 400

        assert "msg" in result_data_missing_username
        assert "msg" in result_data_missing_email
        assert "msg" in result_data_missing_password


def test_handle_register_user_already_existing(app: Flask):
    with app.app_context():
        # given
        user = create_user()
        data_username_existing = {
            "username": user.username,
            "email": "new.email@gmail.com",
            "password": "password"
        }
        data_email_existing = {
            "username": "OtherUsername",
            "email": user.email,
            "password": "password"
        }

        # when
        (result_data_username_existing,
         status_code_username_existing) = auth_controller.handle_register(
             data_username_existing)

        (result_data_email_existing,
         status_code_email_existing) = auth_controller.handle_register(
             data_email_existing)

        # then
        assert status_code_username_existing == 409
        assert status_code_email_existing == 409

        assert "msg" in result_data_username_existing
        assert "msg" in result_data_email_existing


def test_handle_login(app: Flask):
    with app.app_context():
        # given
        PASSWORD = "password"
        user = create_user(password=PASSWORD)
        data_with_username = {
            "username": user.username,
            "password": PASSWORD
        }
        data_with_email = {
            "email": user.email,
            "password": PASSWORD
        }

        # when
        jwt_by_username, status_code_by_username = auth_controller.handle_login(  # noqa
            data_with_username)
        jwt_by_email, status_code_by_email = auth_controller.handle_login(
            data_with_email)

        user_by_username = decode_token(
            jwt_by_username["access_token"]).get("sub")
        user_by_email = decode_token(
            jwt_by_email["access_token"]).get("sub")

        # then
        assert status_code_by_username == 200
        assert status_code_by_email == 200

        assert user_by_username["username"] == user.username
        assert user_by_username["email"] == user.email
        assert user_by_email["username"] == user.username
        assert user_by_email["email"] == user.email
        assert "roles" in user_by_username
        assert "roles" in user_by_email

        assert jwt_by_username is not None
        assert "access_token" in jwt_by_username
        assert "refresh_token" in jwt_by_username
        assert len(jwt_by_username["access_token"]) > 10
        assert len(jwt_by_username["refresh_token"]) > 10

        assert user_by_email is not None
        assert "access_token" in jwt_by_email
        assert "refresh_token" in jwt_by_email
        assert len(jwt_by_email["access_token"]) > 10
        assert len(jwt_by_email["refresh_token"]) > 10


def test_handle_login_missing_username_or_email(app: Flask):
    with app.app_context():
        # given
        user = create_user()
        data = {
            "WrongUsernameKey": user.username,
            "password": "password"
        }

        # when
        result_data, status_code = auth_controller.handle_login(data)

        expected_data = {
            "msg": "The field 'username or email' is required but was null."
        }

        # then
        assert status_code == 400
        assert result_data == expected_data


def test_handle_login_invalid_credentials(app: Flask):
    with app.app_context():
        # given
        PASSWORD = "password"
        user = create_user(password=PASSWORD)
        data_wrong_username = {
            "username": "WrongUsername",
            "password": PASSWORD
        }
        data_wrong_password = {
            "username": user.username,
            "password": "WrongPassword"
        }

        # when
        (result_data_wrong_username,
         status_code_wrong_username) = auth_controller.handle_login(
             data_wrong_username)

        (result_data_wrong_password,
         status_code_wrong_password) = auth_controller.handle_login(
             data_wrong_password)

        expected_data = {
            "msg": "User credentials are invalid."
        }

        # then
        assert status_code_wrong_username == 401
        assert status_code_wrong_password == 401

        assert result_data_wrong_username == expected_data
        assert result_data_wrong_password == expected_data
