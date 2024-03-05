# type: ignore
from werkzeug import exceptions

from typing import Any, Callable

from flask_restx import marshal
from flask import Response
from sqlalchemy import or_, and_
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from flask_sqlalchemy.model import Model

from server.logger import logger
from server.db import db
from server.core.enums import searchtype
from server import redis
from server.api import api
from server.errors import http_errors
from server.errors import errors
from server.utils import helper


class BaseCrudController:

    def __init__(
            self,
            model: Model,
            api_model: api.model,
            api_model_send: api.model = None,
            unique_columns: list[str] = None,
            search_fields: list[str] = None,
            pagination_page_size: int = 20,
            use_redis: bool = True
    ) -> None:
        self._model = model
        self._api_model = api_model
        self._api_model_send = api_model_send
        self._unique_columns = unique_columns
        self._search_fields = search_fields
        self._pagination_page_size = pagination_page_size
        self._use_redis = use_redis

    def handle_get(self, id: Any) -> Response:
        try:
            redis_key = redis.gen_key(self._model)
            if self._use_redis:
                obj = redis.get(redis_key)
                if obj is not None:
                    return obj, 200

            obj = self._find_object_by_id(id)
            response_data = marshal(obj, self._api_model)

            if self._use_redis:
                redis.set(redis_key, response_data)

            return response_data, 200

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_get_list(self, reqargs: dict, query: Query = None) -> Response:
        try:
            redis_key = redis.gen_key(self._model)
            if self._use_redis:
                obj = redis.get(redis_key)
                if obj is not None:
                    return obj, 200

            model_query: Query = query if query else self._model.query

            model_search = self._create_model_search(reqargs=reqargs)

            if model_search is not None:
                model_query = model_query.filter(model_search)

            result_data = self._paginate_model_query(
                model_query=model_query,
                reqargs=reqargs
            )

            response_data = marshal(result_data, self._api_model)

            if self._use_redis:
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
            self,
            data: dict,
            unique_primarykey: Any = None
    ) -> Response:
        try:
            obj = self._model.from_json(data, self._api_model_send)

            self._check_unqiue_column(obj)
            self._ckeck_unique_primarykey(unique_primarykeys=unique_primarykey)

            db.session.add(obj)
            db.session.commit()

            if self._use_redis:
                redis_key_pattern = redis.gen_key(self._model, "*")
                redis.clear_cache(redis_key_pattern)

            return marshal(obj, self._api_model), 201

        except (errors.DbModelValidationException,
                errors.DbModelSerializationException) as e:
            return http_errors.bad_request(e)

        except (errors.DbModelUnqiueConstraintException,
                errors.DbModelAlreadyExistingException) as e:
            return http_errors.conflict(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_patch(self, id: Any, data: dict) -> Response:
        try:
            obj = self._find_object_by_id(id)

            for key, value in data.items():
                if not hasattr(obj, key):
                    err_msg = f"Field '{key}' doen't exist in object '{self._model.__name__}'"  # noqa
                    raise errors.DbModelFieldValueError(err_msg)

                setattr(obj, key, value)

            db.session.commit()

            if self._use_redis:
                redis_key_pattern = redis.gen_key(self._model, "*")
                redis.clear_cache(redis_key_pattern)

            return marshal(obj, self._api_model), 200

        except errors.DbModelValidationException as e:
            return http_errors.bad_request(e)

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_delete(self, id: Any) -> Response:
        try:
            obj = self._find_object_by_id(id)

            db.session.delete(obj)
            db.session.commit()

            if self._use_redis:
                redis_key_pattern = redis.gen_key(self._model, "*")
                redis.clear_cache(redis_key_pattern)

            return None, 204

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def _check_unqiue_column(self, obj: Model) -> None:
        if self._unique_columns is None:
            return

        for column in self._unique_columns:
            obj_attr_value = getattr(obj, column)
            filter_kwargs = {column: obj_attr_value}
            result_count = self._model.query.filter_by(**filter_kwargs).count()
            if result_count > 0:
                raise errors.DbModelUnqiueConstraintException(
                    filedname=column,
                    value=obj_attr_value
                )

    def _ckeck_unique_primarykey(self, unique_primarykeys: tuple[str]) -> None:
        if unique_primarykeys is None:
            return

        obj = self._model.query.get(unique_primarykeys)

        if obj is None:
            return

        raise errors.DbModelAlreadyExistingException(
            model=self._model,
            data=unique_primarykeys
        )

    def _find_object_by_id(self, id: int) -> Model:
        obj = self._model.query.get(id)

        if not obj:
            err_msg = f"Object {self._model.__name__} with id = {id} doesn't exist"  # noqa
            raise errors.DbModelNotFoundException(err_msg)

        return obj

    def _create_model_search(self, reqargs: dict) -> Query:
        if self._search_fields is None:
            return None

        search_type = reqargs.get("search_type", searchtype.EQUALS)
        search_way = reqargs.get("search_way", "and")  # "or" / "and"

        if search_type is None:
            return None

        self._validate_search_type(search_type)
        self._validate_search_way(search_way)

        fn_search_way: Callable = and_ if search_way == "and" else or_
        match search_type:
            case searchtype.EQUALS:
                return fn_search_way(*[
                    getattr(self._model, field) == reqargs.get(field)
                    for field in self._search_fields
                    if reqargs.get(field) is not None
                ])

            case searchtype.CONTAINS:
                return fn_search_way(*[
                    getattr(self._model, field).like(f"%{reqargs.get(field)}%")
                    for field in self._search_fields
                    if reqargs.get(field) is not None
                ])

            case searchtype.STARTS_WITH:
                return fn_search_way(*[
                    getattr(self._model, field).startswith(reqargs.get(field))
                    for field in self._search_fields
                    if reqargs.get(field) is not None
                ])

            case searchtype.ENDS_WITH:
                return fn_search_way(*[
                    getattr(self._model, field).endswith(reqargs.get(field))
                    for field in self._search_fields
                    if reqargs.get(field) is not None
                ])

    def _paginate_model_query(
            self,
            model_query: Query,
            reqargs: dict
    ) -> list:
        page = reqargs.get("page")
        page_size = reqargs.get("page_size", self._pagination_page_size)

        if page is None:
            return model_query.all()

        self._validate_page(page)
        self._validate_page_size(page_size)

        result_pagination: Pagination = model_query.paginate(
            page=int(page),
            per_page=int(page_size)
        )

        return result_pagination.items

    def _validate_page(self, page: int) -> None:
        if not helper.is_integer(page):
            err_msg = "Query parameter 'page' should be type of int."
            raise errors.ValueErrorGeneral(err_msg)

        if int(page) < 1:
            raise errors.PaginationPageException(page)

    def _validate_page_size(self, page_size: int) -> None:
        if not helper.is_integer(page_size):
            err_msg = "Query parameter 'page_size' should be type of int."
            raise errors.ValueErrorGeneral(err_msg)

        if int(page_size) < 1:
            raise errors.PaginationPageSizeException(page_size)

    def _validate_search_type(
            self,
            search_type: str = searchtype.EQUALS
    ) -> None:
        if search_type not in searchtype.ALLOWED_SEARCH_TYPES:
            err_msg = f"The given search_type '{search_type}' is invalid. Use: {str(search_type)}."  # noqa
            raise errors.ValueErrorGeneral(err_msg)

    def _validate_search_way(self, search_way: str = "or") -> None:
        if search_way not in {"or", "and"}:
            err_msg = f"The given search_way '{search_way}' is invalid. Use: ['or', 'and']."  # noqa
            raise errors.ValueErrorGeneral(err_msg)
