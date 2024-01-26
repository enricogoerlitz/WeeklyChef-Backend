from functools import wraps
from dataclasses import dataclass

from flask import jsonify, g
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)


jwt_manager = JWTManager()


@dataclass(frozen=True)
class JsonWebTokenDTO:
    access_token: str
    refresh_token: str

    @staticmethod
    def create(obj: dict) -> 'JsonWebTokenDTO':
        """
        Creates an JsonWebTokenDTO from the given object.

        Args:
            obj (dict): any dictinory as object

        Returns:
            JsonWebTokenDTO: created JsonWebTokenDTO
        """
        access_token = create_access_token(identity=obj)
        refresh_token = create_refresh_token(identity=obj)

        return JsonWebTokenDTO(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def to_dict(self) -> dict:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        }


def jwt_add_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        g.user = get_jwt_identity()
        return f(*args, **kwargs)
    return wrapper


def userrole_required(required_roles: list[str]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user_roles = g.user.roles if hasattr(g, "user") and hasattr(g.user, "roles") else []  # noqa
            if any(role in user_roles for role in required_roles):
                return f(*args, **kwargs)
            else:
                return jsonify(message="Unauthorized. Role required."), 403
        return wrapper
    return decorator


# # Create an endpoint for user login
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")

#     user = find_user_by_username(username)

#     if user and password == user.password:
#         # Identity can be any data that is json serializable
#         access_token = create_access_token(identity=user.to_dict())
#         return jsonify(access_token=access_token), 200

#     return jsonify(message="Invalid credentials"), 401
