"""
Helper for basic CRUD operations
"""
from typing import Any

from flask_restx import marshal
from flask import Response, request

from logger import logger
from db import db
from api import api
from errors import http_errors
from errors import errors


def handle_get(
        model: db.Model,
        api_model: api.model,
        id: Any
) -> Response:
    """_summary_

    Args:
        model (db.Model): _description_
        api_model (api.model): _description_
        id (Any): _description_

    Returns:
        Response: _description_
    """
    try:
        obj = _find_object_by_id(model, id)

        return marshal(obj, api_model), 200

    except errors.DbModelNotFoundException as e:
        return http_errors.bad_request(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_get_list(model: db.Model, api_model: api.model) -> Response:
    """_summary_

    Args:
        model (db.Model): _description_
        api_model (api.model): _description_

    Returns:
        Response: _description_
    """
    try:
        return marshal(model.query.all(), api_model), 200
    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_post(
        model: db.Model,
        api_model: api.model,
        unique_columns: list[str] = None
) -> Response:
    try:
        req_data = request.get_json()
        obj = model.from_json(req_data)

        _check_unqiue_column(
            model=model,
            obj=obj,
            unique_columns=unique_columns
        )

        db.session.add(obj)
        db.session.commit()

        return marshal(obj, api_model), 201

    except errors.DbModelUnqiueConstraintException as e:
        return http_errors.conflict(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_update(
        model: db.Model,
        api_model: api.model,
        id: Any
) -> Response:
    try:
        update_data = request.get_json()

        obj = _find_object_by_id(model, id)

        for key, value in update_data.items():
            if not hasattr(obj, key):
                err_msg = f"Field '{key}' doen't exist in object '{model.__name__}'"  # noqa
                raise errors.DbModelFieldValueError(err_msg)

            setattr(obj, key, value)

        db.session.commit()

        return marshal(obj, api_model), 200

    except (errors.DbModelValidationException,
            errors.DbModelNotFoundException) as e:
        return http_errors.bad_request(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_delete(
        model: db.Model,
        id: Any
) -> Response:
    try:
        obj = _find_object_by_id(model, id)

        db.session.delete(obj)
        db.session.commit()

        return "", 204

    except errors.DbModelNotFoundException as e:
        return http_errors.bad_request(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def _check_unqiue_column(
        model,
        obj,
        unique_columns: list[str]
) -> Exception:
    for column in unique_columns:
        filter_kwargs = {column: obj[column]}
        result_count = model.query.filter_by(**filter_kwargs).count()
        if result_count > 0:
            raise errors.DbModelUnqiueConstraintException(
                filedname=column,
                value=obj[column]
            )


def _find_object_by_id(
        model,
        id
) -> Any:
    obj = model.query.get(id)

    if not obj:
        err_msg = f"Object '{model.__name__}' with id = {id} doesn't exist"  # noqa
        raise errors.DbModelNotFoundException(err_msg)

    return obj