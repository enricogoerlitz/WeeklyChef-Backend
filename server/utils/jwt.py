"""
Module fpr managing app JWT
"""

from functools import wraps
from dataclasses import dataclass

from flask import g
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)

from errors import http_errors


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
            user: dict = get_jwt_identity()
            user_roles = user.get("roles", [])

            if any(role in user_roles for role in required_roles):
                return f(*args, **kwargs)

            exp_msg = f"Unauthorized. Roles {str(required_roles)} required."
            return http_errors.unauthorized(Exception(exp_msg))
        return wrapper
    return decorator
