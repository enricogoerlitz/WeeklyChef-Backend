# type: ignore
from typing import Any

from flask_restx import marshal
from flask import Response

from server.logger import logger
from server.db import db
from server import redis
from server.api import api
from server.errors import http_errors
from server.errors import errors


def handle_get(
        model: db.Model,
        api_model: api.model,
        id: Any,
        use_redis: bool = True
) -> Response:
    try:
        redis_key = redis.gen_key(model)
        if use_redis:
            obj = redis.get(redis_key)
            if obj is not None:
                return obj, 200

        obj = _find_object_by_id(model, id)
        response_data = marshal(obj, api_model)

        if use_redis:
            redis.set(redis_key, response_data)

        return response_data, 200

    except errors.DbModelNotFoundException as e:
        return http_errors.not_found(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_get_list(
        model: db.Model,
        api_model: api.model,
        use_redis: bool = True
) -> Response:  # noqa
    try:
        redis_key = redis.gen_key(model)
        if use_redis:
            obj = redis.get(redis_key)
            if obj is not None:
                return obj, 200

        response_data = marshal(model.query.all(), api_model)

        if use_redis:
            redis.set(redis_key, response_data)

        return response_data, 200
    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_post(
        model: db.Model,
        api_model: api.model,
        api_model_send: api.model,
        data: dict,
        unique_columns: list[str] = None,
        unique_primarykey: Any = None,
        clear_cache: bool = True
) -> Response:
    try:
        obj = model.from_json(data, api_model_send)

        _check_unqiue_column(
            model=model,
            obj=obj,
            unique_columns=unique_columns
        )

        _ckeck_unique_primarykey(
            model=model,
            unique_primarykeys=unique_primarykey
        )

        db.session.add(obj)
        db.session.commit()

        if clear_cache:
            redis_key_pattern = redis.gen_key(model, "*")
            redis.clear_cache(redis_key_pattern)

        return marshal(obj, api_model), 201

    except (errors.DbModelValidationException,
            errors.DbModelSerializationException) as e:
        return http_errors.bad_request(e)

    except (errors.DbModelUnqiueConstraintException,
            errors.DbModelAlreadyExistingException) as e:
        return http_errors.conflict(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_patch(
        model: db.Model,
        api_model: api.model,
        id: Any,
        data: dict,
        clear_cache: bool = True
) -> Response:
    try:
        obj = _find_object_by_id(model, id)

        for key, value in data.items():
            if not hasattr(obj, key):
                err_msg = f"Field '{key}' doen't exist in object '{model.__name__}'"  # noqa
                raise errors.DbModelFieldValueError(err_msg)

            setattr(obj, key, value)

        db.session.commit()

        if clear_cache:
            redis_key_pattern = redis.gen_key(model, "*")
            redis.clear_cache(redis_key_pattern)

        return marshal(obj, api_model), 200

    except errors.DbModelValidationException as e:
        return http_errors.bad_request(e)

    except errors.DbModelNotFoundException as e:
        return http_errors.not_found(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_delete(
        model: db.Model,
        id: Any,
        clear_cache: bool = True
) -> Response:
    try:
        obj = _find_object_by_id(model, id)

        db.session.delete(obj)
        db.session.commit()

        if clear_cache:
            redis_key_pattern = redis.gen_key(model, "*")
            redis.clear_cache(redis_key_pattern)

        return None, 204

    except errors.DbModelNotFoundException as e:
        return http_errors.not_found(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def _check_unqiue_column(
        model,
        obj,
        unique_columns: list[str]
) -> Exception:
    if unique_columns is None:
        return

    for column in unique_columns:
        obj_attr_value = getattr(obj, column)
        filter_kwargs = {column: obj_attr_value}
        result_count = model.query.filter_by(**filter_kwargs).count()
        if result_count > 0:
            raise errors.DbModelUnqiueConstraintException(
                filedname=column,
                value=obj_attr_value
            )


def _ckeck_unique_primarykey(
        model,
        unique_primarykeys: tuple[str]
) -> None:

    if unique_primarykeys is None:
        return

    obj = model.query.get(unique_primarykeys)

    if obj is None:
        return

    raise errors.DbModelAlreadyExistingException(
        model=model,
        data=unique_primarykeys
    )


def _find_object_by_id(
        model,
        id
) -> Any:
    obj = model.query.get(id)

    if not obj:
        err_msg = f"Object {model.__name__} with id = {id} doesn't exist"  # noqa
        raise errors.DbModelNotFoundException(err_msg)

    return obj
