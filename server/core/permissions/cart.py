from functools import wraps

from flask import request

from sqlalchemy import and_

from server.utils import jwt
from server.errors import http_errors
from server.core.models.db_models.cart import Cart, UserSharedEditCart


def IsCartOwnerOrCanEdit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        cart_id = request.view_args.get("id")

        is_user_owner = Cart.query.filter(
            and_(
                Cart.id == cart_id,
                Cart.owner_user_id == user_id
            )
        ).count() == 1

        can_user_edit = UserSharedEditCart.query.filter(
            and_(
                UserSharedEditCart.cart_id == cart_id,
                UserSharedEditCart.user_id == user_id
            )
        ).count() == 1

        if is_user_owner or can_user_edit:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper


def IsCartOwner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        cart_id = request.view_args.get("id")

        is_user_owner = Cart.query.filter(
            and_(
                Cart.id == cart_id,
                Cart.owner_user_id == user_id
            )
        ).count() == 1

        if is_user_owner:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper
