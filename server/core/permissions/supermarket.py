from functools import wraps

from flask import request

from sqlalchemy import and_

from server.errors import errors
from server.utils import jwt
from server.errors import http_errors
from server.core.models.db_models.supermarket import (
    Supermarket, UserSharedEditSupermarket
)


def IsSupermarketOwnerOrCanEdit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        supermarket_id = request.view_args.get("id")

        if Supermarket.query.get(supermarket_id) is None:
            e = errors.DbModelNotFoundException(
                model=Supermarket,
                id=supermarket_id
            )
            return http_errors.not_found(e)

        is_user_owner = Supermarket.query.filter(
            and_(
                Supermarket.id == supermarket_id,
                Supermarket.owner_user_id == user_id
            )
        ).count() == 1

        can_user_edit = UserSharedEditSupermarket.query.filter(
            and_(
                UserSharedEditSupermarket.supermarket_id == supermarket_id,
                UserSharedEditSupermarket.user_id == user_id
            )
        ).count() == 1

        if is_user_owner or can_user_edit:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper


def IsSupermarketOwner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        supermarket_id = request.view_args.get("id")

        if Supermarket.query.get(supermarket_id) is None:
            e = errors.DbModelNotFoundException(
                model=Supermarket,
                id=supermarket_id
            )
            return http_errors.not_found(e)

        is_user_owner = Supermarket.query.filter(
            and_(
                Supermarket.id == supermarket_id,
                Supermarket.owner_user_id == user_id
            )
        ).count() == 1

        if is_user_owner:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper
