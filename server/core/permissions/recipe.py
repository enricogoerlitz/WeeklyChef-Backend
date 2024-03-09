from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity
from sqlalchemy import and_

from server.core.models.db_models.recipe import Recipe
from server.errors import http_errors
from server.core.enums import roles
from server.core.permissions.general import unauthorized_error


def IsRecipeCreatorOrAdminOrStaff(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        jwt_identity = get_jwt_identity()
        recipe_id = request.view_args.get("id")
        user_id = jwt_identity["id"]
        user_roles = jwt_identity["roles"]

        if roles.ADMIN in user_roles or roles.STAFF in user_roles:
            return func(*args, **kwargs)

        is_creator_user_count = Recipe.query.filter(
            and_(
                Recipe.id == recipe_id,
                Recipe.creator_user_id == user_id
            )
        ).count()

        if is_creator_user_count > 0:
            return func(*args, **kwargs)

        return http_errors.unauthorized(
            unauthorized_error(
                authorized_roles=[roles.ADMIN]
            )
        )

    return wrapper
