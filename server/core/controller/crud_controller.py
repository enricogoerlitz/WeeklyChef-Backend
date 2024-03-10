# type: ignore
from werkzeug import exceptions
from typing import Any, Callable
from abc import ABC, abstractmethod

from flask_restx import marshal
from flask import Response
from sqlalchemy import or_, and_
from flask_sqlalchemy.pagination import Pagination
from flask_sqlalchemy.query import Query
from flask_sqlalchemy.model import Model

from server.logger import logger
from server.db import db
from server.core.enums import searchtype
from server.caching.redis import api_cache
from server.api import api
from server.errors import http_errors
from server.errors import errors
from server.utils import helper


class IController(ABC):

    @abstractmethod
    def handle_get_list(self): pass

    @abstractmethod
    def handle_get(self): pass

    @abstractmethod
    def handle_post(self): pass

    @abstractmethod
    def handle_patch(self): pass

    @abstractmethod
    def handle_delete(self): pass


class AbstractRedisCache:

    def __init__(
            self,
            model: Model,
            use_caching: bool,
            clear_cache_models: list[Model] = None
    ) -> None:
        self._main_model = model
        self._use_caching = use_caching

        clear_cache_models = clear_cache_models if clear_cache_models else []
        self._clear_cache_models = list(set([self._main_model] + clear_cache_models))  # noqa

    # protected
    def _get_cache(self, redis_addition_key: str | None) -> Any:
        if not self._use_caching:
            return None

        redis_key = api_cache.gen_key(
            self._main_model, redis_addition_key=redis_addition_key)

        return api_cache.get(redis_key)

    # protected
    def _set_cache(self, data: Any, redis_addition_key: str | None) -> None:
        redis_key = api_cache.gen_key(
            self._main_model, redis_addition_key=redis_addition_key)
        if self._use_caching:
            api_cache.set(redis_key, data)

    # protected
    def _clear_cache(self) -> None:
        if not self._use_caching:
            return

        for model in self._clear_cache_models:
            redis_key_pattern = api_cache.gen_key(model, "*")
            api_cache.clear_cache(redis_key_pattern)


class BaseCrudController(IController, AbstractRedisCache):

    def __init__(
            self,
            *,
            model: Model,
            api_model: api.model,
            api_model_send: api.model,
            api_model_detail: api.model = None,
            unique_columns: list[str] = None,
            unique_columns_together: list[list[str]] | list[str] = None,
            foreign_key_columns: list[tuple[Model, Any]] = None,
            read_only_fields: list[str] = None,
            search_fields: list[str] = None,
            pagination_page_size: int = 20,
            use_caching: bool = True,
            clear_cache_models: list[Model] = None
    ) -> None:
        AbstractRedisCache.__init__(
            self,
            model=model,
            use_caching=use_caching,
            clear_cache_models=clear_cache_models
        )
        self._model = model
        self._api_model = api_model
        self._api_model_send = api_model_send
        self._api_model_detail = api_model_detail if api_model_detail else api_model  # noqa
        self._unique_columns = unique_columns
        self._search_fields = search_fields
        self._pagination_page_size = pagination_page_size
        self._read_only_fields = read_only_fields
        self._foreign_key_columns = foreign_key_columns
        self._unique_columns_together = unique_columns_together

    def handle_get(
            self,
            id: Any,
            redis_addition_key: str = None,  # like user_id
            api_response_model: str = None
    ) -> Response:
        try:
            cache_obj = self._get_cache(redis_addition_key)
            if cache_obj is not None:
                return cache_obj, 200

            obj = self._find_object_by_id(id)

            api_response_model = api_response_model if api_response_model else self._api_model_detail  # noqa
            response_data = marshal(obj, api_response_model)

            self._set_cache(response_data, redis_addition_key)

            return response_data, 200

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_get_list(
            self,
            reqargs: dict,
            query: Query = None,
            redis_addition_key: str = None,  # like user_id
            api_response_model: str = None
    ) -> Response:
        try:
            cache_obj = self._get_cache(redis_addition_key)
            if cache_obj is not None:
                return cache_obj, 200

            model_query: Query = query if query else self._model.query

            model_search = self._create_model_search(reqargs=reqargs)

            if model_search is not None:
                model_query = model_query.filter(model_search)

            result_data = self._paginate_model_query(
                model_query=model_query,
                reqargs=reqargs
            )

            api_response_model = api_response_model if api_response_model else self._api_model  # noqa
            response_data = marshal(result_data, api_response_model)

            self._set_cache(response_data, redis_addition_key)

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

            self._check_foreignkeys_existing(data)
            self._check_unqiue_column(data)
            self._check_unique_columns_together(data)
            self._ckeck_unique_primarykey(unique_primarykey)

            db.session.add(obj)
            db.session.commit()

            self._clear_cache()

            return marshal(obj, self._api_model), 201

        except (errors.DbModelValidationException,
                errors.DbModelSerializationException) as e:
            return http_errors.bad_request(e)

        except errors.ForeignkeyNotFoundException as e:
            return http_errors.not_found(e)

        except (errors.DbModelUnqiueConstraintException,
                errors.DbModelAlreadyExistingException) as e:
            return http_errors.conflict(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_patch(self, id: Any, data: dict) -> Response:
        try:
            obj = self._find_object_by_id(id)

            self._check_read_only_fields(data)
            self._check_foreignkeys_existing(data)
            self._check_unqiue_column(data)
            self._check_unique_columns_together(
                data=data,
                current_obj=obj
            )

            for key, value in data.items():
                if not hasattr(obj, key):
                    err_msg = f"Field '{key}' doen't exist in object '{self._model.__name__}'"  # noqa
                    raise errors.DbModelFieldValueError(err_msg)

                setattr(obj, key, value)

            db.session.commit()

            self._clear_cache()

            return marshal(obj, self._api_model), 200

        except (errors.DbModelValidationException,
                errors.ReadOnlyFieldInPayloadException) as e:
            return http_errors.bad_request(e)

        except (errors.DbModelNotFoundException,
                errors.ForeignkeyNotFoundException) as e:
            return http_errors.not_found(e)

        except errors.DbModelUnqiueConstraintException as e:
            return http_errors.conflict(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_delete(self, id: Any) -> Response:
        try:
            obj = self._find_object_by_id(id)

            db.session.delete(obj)
            db.session.commit()

            self._clear_cache()

            return None, 204

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def _check_foreignkeys_existing(self, data: dict) -> None:
        if self._foreign_key_columns is None:
            return

        model: Model
        for model, field in self._foreign_key_columns:
            if field not in data.keys():
                continue

            id = data[field]
            obj = model.query.get(id)

            if obj is None:
                err_msg = f"Foreignkey '{field}={id}' is not existing for model '{model.__name__}'."  # noqa
                raise errors.ForeignkeyNotFoundException(err_msg)

    def _check_unqiue_column(self, data: dict) -> None:
        if self._unique_columns is None:
            return

        for column in self._unique_columns:
            value = data.get(column)
            filter_kwargs = {column: value}
            result_count = self._model.query.filter_by(**filter_kwargs).count()

            if result_count > 0:
                raise errors.DbModelUnqiueConstraintException(
                    filedname=column,
                    value=value
                )

    def _check_unique_columns_together(
            self,
            data: dict,
            current_obj: Model = None
    ) -> None:
        if self._unique_columns_together is None or len(self._unique_columns_together) == 0:  # noqa
            return

        unique_columns_list = ([self._unique_columns_together]
                               if isinstance(self._unique_columns_together[0], str)  # noqa
                               else self._unique_columns_together)

        for unique_columns in unique_columns_list:
            filter_kwargs = {}
            for field in unique_columns:
                value = data.get(field, None)
                filter_kwargs |= {field: value}

            result_count = self._model.query.filter_by(**filter_kwargs).count()

            if result_count == 0:
                continue

            if result_count == 1 and current_obj is not None:
                result_model = self._model.query.filter_by(**filter_kwargs).first()  # noqa
                if result_model == current_obj:
                    continue

            err_fields = str(filter_kwargs)
            err_msg = f"The given fields are alredy existing with these values: {err_fields}."  # noqa
            raise errors.DbModelUnqiueConstraintException(msg=err_msg)

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
            raise errors.DbModelNotFoundException(
                model=self._model,
                id=id
            )

        return obj

    def _create_model_search(self, reqargs: dict) -> Query:
        if self._search_fields is None or reqargs is None:
            return None

        search_type = reqargs.get("search_type", searchtype.EQUALS)
        search_way = reqargs.get("search_way", "and")

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
        if reqargs is None:
            return model_query.all()

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

    def _check_read_only_fields(self, data: dict) -> None:
        if self._read_only_fields is None:
            return

        for field in self._read_only_fields:
            if field in data:
                raise errors.ReadOnlyFieldInPayloadException(field)

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
