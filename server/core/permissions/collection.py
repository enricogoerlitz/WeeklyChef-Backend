from functools import wraps

from flask import request

from sqlalchemy import and_

from server.utils import jwt
from server.errors import http_errors
from server.core.models.db_models.collection import (
    Collection, UserSharedCollection
)


def IsCollectionOwnerOrHasAccess(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        collection_id = request.view_args.get("id")

        is_user_owner = Collection.query.filter(
            and_(
                Collection.id == collection_id,
                Collection.owner_user_id == user_id
            )
        ).count() == 1

        has_user_access = UserSharedCollection.query.filter(
            and_(
                UserSharedCollection.collection_id == collection_id,
                UserSharedCollection.user_id == user_id
            )
        ).count() == 1

        if is_user_owner or has_user_access:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper


def IsCollectionOwnerOrCanEdit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        collection_id = request.view_args.get("id")

        is_user_owner = Collection.query.filter(
            and_(
                Collection.id == collection_id,
                Collection.owner_user_id == user_id
            )
        ).count() == 1

        can_user_edit = UserSharedCollection.query.filter(
            and_(
                UserSharedCollection.collection_id == collection_id,
                UserSharedCollection.user_id == user_id,
                UserSharedCollection.can_edit == True  # noqa
            )
        ).count() == 1

        if is_user_owner or can_user_edit:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper


def IsCollectionOwner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        collection_id = request.view_args.get("id")

        is_user_owner = Collection.query.filter(
            and_(
                Collection.id == collection_id,
                Collection.owner_user_id == user_id
            )
        ).count() == 1

        if is_user_owner:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper
