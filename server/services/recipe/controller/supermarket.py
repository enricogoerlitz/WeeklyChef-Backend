from flask import Response
from flask_restx import marshal
from sqlalchemy import or_, and_

from server.errors import errors
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.supermarket import (
    Supermarket, SupermarketArea,
    SupermarketAreaIngredientComposite, UserSharedEditSupermarket)
from server.core.models.api_models.supermarket import (
    supermarket_area_ingredinet_model,
    supermarket_area_ingredinet_model_send,
    supermarket_area_model, supermarket_area_model_send,
    supermarket_model, supermarket_model_detail, supermarket_model_send,
    supermarket_user_edit_model)
from server.core.models.db_models.ingredient import Ingredient
from server.errors import http_errors
from server.logger import logger
from server.db import db


class SupermarketController(BaseCrudController):

    def handle_get_list(
            self,
            reqargs: dict,
            api_response_model: db.Model = None  # type: ignore
    ) -> Response:
        try:
            search = reqargs.get("search")
            logger.debug(f"SEARCH: {search}")

            if search is None:
                return super().handle_get_list(
                    reqargs=reqargs,
                    api_response_model=api_response_model
                )

            search_str = f"%{search}%"
            query = self._model.query.filter(
                or_(
                    Supermarket.name.like(search_str),
                    Supermarket.street.like(search_str),
                    Supermarket.postcode.like(search_str),
                    Supermarket.district.like(search_str)
                )
            )

            return super().handle_get_list(
                reqargs=reqargs,
                query=query,
                api_response_model=api_response_model
            )

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT


class SupermarketAreaController(BaseCrudController):
    _model: SupermarketArea

    def handle_get_list(
            self,
            reqargs: dict,
            supermarket_id: int
    ) -> Response:
        try:
            query = self._model.query.filter(
                self._model.supermarket_id == supermarket_id)

            return super().handle_get_list(
                reqargs=reqargs,
                query=query
            )
        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_post_change_order(
            self,
            id: int,
            new_order_number: int
    ) -> Response:
        try:
            area_obj: SupermarketArea = self._find_object_by_id(id)

            if new_order_number == area_obj.order_number:
                return marshal(area_obj, self._api_model)

            inc_number = 1
            if new_order_number > area_obj.order_number:
                updating_areas = self._model.query.filter(
                    and_(
                        self._model.supermarket_id == area_obj.supermarket_id,
                        self._model.order_number > area_obj.order_number,
                        self._model.order_number <= new_order_number
                    )
                ).all()
                inc_number = -1
            else:
                updating_areas = self._model.query.filter(
                    and_(
                        self._model.supermarket_id == area_obj.supermarket_id,
                        self._model.order_number < area_obj.order_number,
                        self._model.order_number >= new_order_number
                    )
                ).all()

            updating_area: SupermarketArea
            for updating_area in updating_areas:
                updating_area.order_number += inc_number

            area_obj.order_number = new_order_number

            db.session.commit()

            self._clear_cache()

            return marshal(area_obj, self._api_model)

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT


class SupermarketAreaIngredientController(BaseCrudController):
    pass


class UserSharedEditSupermarketController(BaseCrudController):
    pass


supermarket_controller = SupermarketController(
    model=Supermarket,
    api_model=supermarket_model,
    api_model_detail=supermarket_model_detail,
    api_model_send=supermarket_model_send,
    read_only_fields=["owner_user_id"],
    unique_columns_together=["name", "street"]
)

supermarket_area_controller = SupermarketAreaController(
    model=SupermarketArea,
    api_model=supermarket_area_model,
    api_model_send=supermarket_area_model_send,
    foreign_key_columns=[
        (Supermarket, "supermarket_id")
    ],
    unique_columns_together=[
        ["supermarket_id", "name"],
        ["supermarket_id", "order_number"]
    ],
    read_only_fields=["order_number"],
    clear_cache_models=[Supermarket]
)

supermarket_area_ingredient_controller = SupermarketAreaIngredientController(
    model=SupermarketAreaIngredientComposite,
    api_model=supermarket_area_ingredinet_model,
    api_model_send=supermarket_area_ingredinet_model_send,
    foreign_key_columns=[
        (SupermarketArea, "sarea_id"),
        (Ingredient, "ingredient_id")
    ],
    read_only_fields=[
        "sarea_id",
        "ingredient_id"
    ],
    unique_columns_together=[
        "sarea_id",
        "ingredient_id"
    ],
    clear_cache_models=[Supermarket, SupermarketArea]
)

user_shared_edit_supermarket_controller = UserSharedEditSupermarketController(
    model=UserSharedEditSupermarket,
    api_model=supermarket_user_edit_model,
    api_model_send=supermarket_user_edit_model,
    foreign_key_columns=[
        (Supermarket, "supermarket_id")
    ]
)
