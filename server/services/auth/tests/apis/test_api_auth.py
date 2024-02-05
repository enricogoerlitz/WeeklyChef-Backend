import json

from flask import Flask, testing
from flask_jwt_extended.utils import decode_token

from server.db import db
from server.core.models.db_models import User


ROUTE = "/api/v1/auth"


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


# TEST REGISTER

def test_register_post(
        app: Flask,
        client: testing.FlaskClient
):
    with app.app_context():
        # given
        data = {
            "username": "TestUsername",
            "email": "test@email.com",
            "password": "password"
        }
        api_route = f"{ROUTE}/register"

        # when
        response = client.post(api_route, json=data)

        result_data = json.loads(response.data)
        expected_data = data.copy()

        # then
        assert response.status_code == 200
        assert "access_token" in result_data
        assert "refresh_token" in result_data

        access_token_dict = decode_token(result_data["access_token"]).get("sub")  # noqa
        assert "id" in access_token_dict
        assert access_token_dict["username"] == expected_data["username"]
        assert access_token_dict["email"] == expected_data["email"]


def test_register_post_user_already_existing(
        app: Flask,
        client: testing.FlaskClient
):
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

        api_route = f"{ROUTE}/register"

        # when
        response_username_existing = client.post(
            api_route, json=data_username_existing)
        response_email_existing = client.post(
            api_route, json=data_email_existing)

        result_data_username_existing = json.loads(
            response_username_existing.data)
        result_data_email_existing = json.loads(
            response_email_existing.data)

        # then
        assert response_username_existing.status_code == 409
        assert response_email_existing.status_code == 409

        assert "msg" in result_data_username_existing
        assert "msg" in result_data_email_existing


def test_register_post_missing_data(
        app: Flask,
        client: testing.FlaskClient
):
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
        api_route = f"{ROUTE}/register"

        # when
        response_missing_username = client.post(api_route, json=data_missing_username)  # noqa
        response_missing_email = client.post(api_route, json=data_missing_email)  # noqa
        response_missing_password = client.post(api_route, json=data_missing_password)  # noqa

        result_data_missing_username = json.loads(response_missing_username.data)  # noqa
        result_data_missing_email = json.loads(response_missing_email.data)
        result_data_missing_password = json.loads(response_missing_password.data)  # noqa

        # then
        assert response_missing_username.status_code == 400
        assert response_missing_email.status_code == 400
        assert response_missing_password.status_code == 400

        assert "msg" in result_data_missing_username
        assert "msg" in result_data_missing_email
        assert "msg" in result_data_missing_password


# TEST LOGIN

def test_login_post(
        app: Flask,
        client: testing.FlaskClient
):
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
        api_route = f"{ROUTE}/token"

        # when
        response_by_username = client.post(api_route, json=data_with_username)
        response_by_email = client.post(api_route, json=data_with_email)

        result_data_by_username = json.loads(response_by_username.data)
        result_data_by_email = json.loads(response_by_email.data)

        user_by_username = decode_token(
            result_data_by_username["access_token"]).get("sub")
        user_by_email = decode_token(
            result_data_by_email["access_token"]).get("sub")

        # then
        assert response_by_username.status_code == 200
        assert response_by_email.status_code == 200

        assert user_by_username["username"] == user.username
        assert user_by_username["email"] == user.email
        assert user_by_email["username"] == user.username
        assert user_by_email["email"] == user.email
        assert "roles" in user_by_username
        assert "roles" in user_by_email

        assert result_data_by_username is not None
        assert "access_token" in result_data_by_username
        assert "refresh_token" in result_data_by_username
        assert len(result_data_by_username["access_token"]) > 10
        assert len(result_data_by_username["refresh_token"]) > 10

        assert user_by_email is not None
        assert "access_token" in result_data_by_email
        assert "refresh_token" in result_data_by_email
        assert len(result_data_by_email["access_token"]) > 10
        assert len(result_data_by_email["refresh_token"]) > 10


def test_login_post_missing_username_or_email(
        app: Flask,
        client: testing.FlaskClient
):
    with app.app_context():
        # given
        user = create_user()
        data = {
            "WrongUsernameKey": user.username,
            "password": "password"
        }
        api_route = f"{ROUTE}/token"

        # when
        response = client.post(api_route, json=data)

        result_data = json.loads(response.data)

        # then
        assert response.status_code == 400
        assert "msg" in result_data


def test_login_post_invalid_credentials(
        app: Flask,
        client: testing.FlaskClient
):
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
        api_route = f"{ROUTE}/token"

        # when
        response_wrong_username = client.post(
            api_route, json=data_wrong_username)
        response_wrong_password = client.post(
            api_route, json=data_wrong_password)

        result_data_wrong_username = json.loads(response_wrong_username.data)  # noqa
        result_data_wrong_password = json.loads(response_wrong_password.data)  # noqa

        # then
        assert response_wrong_username.status_code == 401
        assert response_wrong_password.status_code == 401

        assert result_data_wrong_username["msg"] == "User credentials are invalid."  # noqa
        assert result_data_wrong_password["msg"] == "User credentials are invalid."  # noqa
