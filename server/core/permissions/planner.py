from functools import wraps

from flask import request

from sqlalchemy import and_

from server.errors import errors
from server.utils import jwt
from server.errors import http_errors
from server.core.models.db_models.planner import (
    RecipePlanner, UserSharedRecipePlanner
)


def IsRecipePlannerOwnerOrHasAccess(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        rplanner_id = request.view_args.get("id")

        if RecipePlanner.query.get(rplanner_id) is None:
            e = errors.DbModelNotFoundException(
                model=RecipePlanner,
                id=rplanner_id
            )
            return http_errors.not_found(e)

        is_user_owner = RecipePlanner.query.filter(
            and_(
                RecipePlanner.id == rplanner_id,
                RecipePlanner.owner_user_id == user_id
            )
        ).count() == 1

        has_user_access = UserSharedRecipePlanner.query.filter(
            and_(
                UserSharedRecipePlanner.rplanner_id == rplanner_id,
                UserSharedRecipePlanner.user_id == user_id
            )
        ).count() == 1

        if is_user_owner or has_user_access:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper


def IsRecipePlannerOwnerOrCanEdit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        rplanner_id = request.view_args.get("id")

        if RecipePlanner.query.get(rplanner_id) is None:
            e = errors.DbModelNotFoundException(
                model=RecipePlanner,
                id=rplanner_id
            )
            return http_errors.not_found(e)

        is_user_owner = RecipePlanner.query.filter(
            and_(
                RecipePlanner.id == rplanner_id,
                RecipePlanner.owner_user_id == user_id
            )
        ).count() == 1

        can_user_edit = UserSharedRecipePlanner.query.filter(
            and_(
                UserSharedRecipePlanner.rplanner_id == rplanner_id,
                UserSharedRecipePlanner.user_id == user_id,
                UserSharedRecipePlanner.can_edit == True  # noqa
            )
        ).count() == 1

        if is_user_owner or can_user_edit:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper


def IsRecipePlannerOwner(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = jwt.get_user_id()
        rplanner_id = request.view_args.get("id")

        if RecipePlanner.query.get(rplanner_id) is None:
            e = errors.DbModelNotFoundException(
                model=RecipePlanner,
                id=rplanner_id
            )
            return http_errors.not_found(e)

        is_user_owner = RecipePlanner.query.filter(
            and_(
                RecipePlanner.id == rplanner_id,
                RecipePlanner.owner_user_id == user_id
            )
        ).count() == 1

        if is_user_owner:
            return func(*args, **kwargs)

        return http_errors.unauthorized()

    return wrapper
