# type: ignore
from werkzeug import exceptions

from typing import Any, Callable

from flask_restx import marshal
from flask import Response
from sqlalchemy import or_, and_
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query

from server.logger import logger
from server.db import db
from server.core.enums import searchtype
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
        reqargs: dict,
        page_size: int = 20,
        search_fields: list[str] = None,
        use_redis: bool = True
) -> Response:
    try:
        redis_key = redis.gen_key(model)
        if use_redis:
            obj = redis.get(redis_key)
            if obj is not None:
                return obj, 200

        model_query: Query = model.query

        model_search = _create_model_search(
            model=model,
            search_fields=search_fields,
            reqargs=reqargs
        )

        if model_search is not None:
            model_query = model_query.filter(model_search)

        result_data = _paginate_model_query(
            model_query=model_query,
            reqargs=reqargs,
            page_size=page_size
        )

        response_data = marshal(result_data, api_model)

        if use_redis:
            redis.set(redis_key, response_data)

        return response_data, 200

    except exceptions.NotFound:
        # pagination page could not found any data
        return [], 200

    except (errors.ValueErrorGeneral,
            errors.PaginationPageException,
            errors.PaginationPageSizeException) as e:
        return http_errors.bad_request(e)

    except Exception as e:
        logger.error(f"{str(e)}")
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


def _create_model_search(
        model: db.Model,
        search_fields: list[str],
        reqargs: dict
) -> Query:
    if search_fields is None:
        return None

    search_type = reqargs.get("search_type", searchtype.EQUALS)
    search_way = reqargs.get("search_way", "and")  # "or" / "and"

    if search_type is None:
        return None

    _validate_search_type(search_type)
    _validate_search_way(search_way)

    fn_search_way: Callable = and_ if search_way == "and" else or_
    match search_type:
        case searchtype.EQUALS:
            return fn_search_way(*[
                getattr(model, field) == reqargs.get(field)
                for field in search_fields
                if reqargs.get(field) is not None
            ])

        case searchtype.CONTAINS:
            return fn_search_way(*[
                getattr(model, field).like(f"%{reqargs.get(field)}%")
                for field in search_fields
                if reqargs.get(field) is not None
            ])

        case searchtype.STARTS_WITH:
            return fn_search_way(*[
                getattr(model, field).startswith(reqargs.get(field))
                for field in search_fields
                if reqargs.get(field) is not None
            ])

        case searchtype.ENDS_WITH:
            return fn_search_way(*[
                getattr(model, field).endswith(reqargs.get(field))
                for field in search_fields
                if reqargs.get(field) is not None
            ])


def _paginate_model_query(
        model_query: Query,
        reqargs: dict,
        page_size
) -> list:
    page = reqargs.get("page")
    page_size = reqargs.get("page_size", page_size)

    if page is None:
        return model_query.all()

    _validate_page(page)
    _validate_page_size(page_size)
    result_pagination: Pagination = model_query.paginate(
        page=int(page),
        per_page=int(page_size)
    )

    return result_pagination.items


def _validate_page(
        page: int
) -> None:
    if not _is_integer(page):
        err_msg = "Query parameter 'page' should be type of int."
        raise errors.ValueErrorGeneral(err_msg)

    if int(page) < 1:
        raise errors.PaginationPageException(page)


def _validate_page_size(
        page_size: int
) -> None:
    if not _is_integer(page_size):
        err_msg = "Query parameter 'page_size' should be type of int."
        raise errors.ValueErrorGeneral(err_msg)

    if int(page_size) < 1:
        raise errors.PaginationPageSizeException(page_size)


def _validate_search_type(search_type: str = searchtype.EQUALS) -> None:
    if search_type not in searchtype.ALLOWED_SEARCH_TYPES:
        err_msg = f"The given search_type '{search_type}' is invalid. Use: {str(search_type)}."  # noqa
        raise errors.ValueErrorGeneral(err_msg)


def _validate_search_way(search_way: str = "or") -> None:
    if search_way not in ["or", "and"]:
        err_msg = f"The given search_way '{search_way}' is invalid. Use: ['or', 'and']."  # noqa
        raise errors.ValueErrorGeneral(err_msg)


# TODO: auslagern!
def _is_integer(
        value: int
) -> bool:
    try:
        int(value)
        return True
    except Exception:
        return False
