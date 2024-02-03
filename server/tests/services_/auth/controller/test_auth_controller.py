import pytest

from flask import Flask

from db import db
from errors import errors
from services.auth.controller import auth_controller
from core.models.db_models import User
from core.enums import roles


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
        user, jwt = auth_controller.handle_register(data)

        jwt_data = jwt.to_dict()

        # then
        assert user is not None
        assert user.password != data["password"]
        assert user.check_password(data["password"])
        assert user.username == data["username"]
        assert user.email == data["email"]
        assert len(user.roles) == 1
        assert user.roles[0].name == roles.STANDARD

        assert jwt is not None
        assert "access_token" in jwt_data
        assert "refresh_token" in jwt_data
        assert len(jwt_data["access_token"]) > 10
        assert len(jwt_data["refresh_token"]) > 10


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

        # when + then
        with pytest.raises(errors.DbModelFieldRequieredException):
            auth_controller.handle_register(data_missing_username)

        with pytest.raises(errors.DbModelFieldRequieredException):
            auth_controller.handle_register(data_missing_email)

        with pytest.raises(errors.DbModelFieldRequieredException):
            auth_controller.handle_register(data_missing_password)


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

        # when + then
        with pytest.raises(errors.UserAlreadyExistingException):
            auth_controller.handle_register(data_username_existing)

        with pytest.raises(errors.UserAlreadyExistingException):
            auth_controller.handle_register(data_email_existing)


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
        user_by_username, jwt_by_username = auth_controller.handle_login(
            data_with_username)
        user_by_email, jwt_by_email = auth_controller.handle_login(
            data_with_email)

        jwt_by_username_data = jwt_by_username.to_dict()
        jwt_by_email_data = jwt_by_email.to_dict()

        # then
        assert user_by_username.username == user.username
        assert user_by_username.email == user.email
        assert user_by_email.username == user.username
        assert user_by_email.email == user.email

        assert jwt_by_username is not None
        assert "access_token" in jwt_by_username_data
        assert "refresh_token" in jwt_by_username_data
        assert len(jwt_by_username_data["access_token"]) > 10
        assert len(jwt_by_username_data["refresh_token"]) > 10

        assert user_by_email is not None
        assert "access_token" in jwt_by_email_data
        assert "refresh_token" in jwt_by_email_data
        assert len(jwt_by_email_data["access_token"]) > 10
        assert len(jwt_by_email_data["refresh_token"]) > 10


def test_handle_login_missing_username_or_email(app: Flask):
    with app.app_context():
        # given
        user = create_user()
        data = {
            "WrongUsernameKey": user.username,
            "password": "password"
        }

        # when + then
        with pytest.raises(errors.DbModelFieldRequieredException):
            auth_controller.handle_login(data)


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

        # when + then
        with pytest.raises(errors.InvalidLoginCredentialsException):
            auth_controller.handle_login(data_wrong_username)

        with pytest.raises(errors.InvalidLoginCredentialsException):
            auth_controller.handle_login(data_wrong_password)
