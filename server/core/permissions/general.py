"""
"""

from functools import wraps
from flask_jwt_extended import get_jwt_identity

from errors import http_errors
from utils import roles


def IsAdmin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt_identity = get_jwt_identity()
        user_roles = jwt_identity["roles"]

        if roles.ADMIN in user_roles:
            return func(*args, **kwargs)

        return http_errors.unauthorized(
            _unauthorized_error(
                authorized_roles=[roles.ADMIN]
            )
        )

    return wrapper


def IsAdminOrStaff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt_identity = get_jwt_identity()
        user_roles = list(jwt_identity["roles"])

        if roles.ADMIN in user_roles or roles.STAFF in user_roles:
            return func(*args, **kwargs)

        return http_errors.unauthorized(
            _unauthorized_error(
                authorized_roles=[roles.ADMIN, roles.STAFF]
            )
        )

    return wrapper


def _unauthorized_error(authorized_roles: list[str]):
    auth_roles_str = ", ".join(authorized_roles)
    msg = f"User is unauthorized. Needed permissions: '{auth_roles_str}'"
    return msg
