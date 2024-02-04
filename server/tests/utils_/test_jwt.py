from flask import Flask
from flask_jwt_extended.utils import decode_token

from server.utils.jwt import JsonWebTokenDTO
from server.core.enums import roles


def test_jwt_dto_create(app: Flask):
    with app.app_context():
        # given
        identity = {
            "username": "TestUsername",
            "email": "test@email.com",
            "roles": [
                roles.STANDARD,
                roles.STAFF
            ]
        }

        # when
        jwt = JsonWebTokenDTO.create(identity)
        result_data = decode_token(jwt.access_token).get("sub")

        expected_data = identity.copy()

        # then
        assert isinstance(jwt, JsonWebTokenDTO)
        assert result_data == expected_data
        assert len(jwt.refresh_token) > 10


def test_jwt_dto_create_obj_is_none(app: Flask):
    with app.app_context():
        # given
        identity = None

        # when
        jwt = JsonWebTokenDTO.create(identity)
        result_data = decode_token(jwt.access_token).get("sub")

        expected_data = identity

        # then
        assert isinstance(jwt, JsonWebTokenDTO)
        assert result_data == expected_data
        assert len(jwt.refresh_token) > 10


def test_jwt_dto_to_dict(app: Flask):
    with app.app_context():
        # given
        identity = {
            "username": "TestUsername",
            "email": "test@email.com",
            "roles": [
                roles.STANDARD,
                roles.STAFF
            ]
        }

        # when
        jwt = JsonWebTokenDTO.create(identity)
        jwt_dict = jwt.to_dict()
        result_data = decode_token(jwt_dict.get("access_token")).get("sub")

        expected_data = identity.copy()

        # then
        assert isinstance(jwt, JsonWebTokenDTO)
        assert isinstance(jwt_dict, dict)
        assert "access_token" in jwt_dict.keys()
        assert "refresh_token" in jwt_dict.keys()
        assert result_data == expected_data
        assert len(jwt_dict["refresh_token"]) > 10
