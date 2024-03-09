from typing import Any
from datetime import date
from dateutil import parser

from flask import Response
from flask_restx import marshal
from sqlalchemy import and_

from server.errors import errors
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.planner.planner import (
    RecipePlanner, RecipePlannerItem,
    UserSharedRecipePlanner)
from server.core.models.api_models.planner import (
    recipe_planner_item_model,
    recipe_planner_item_model_send, recipe_planner_model,
    recipe_planner_model_send,
    user_shared_recipe_planner_model,
    user_shared_recipe_planner_model_send)
from server.core.models.db_models.recipe.recipe import Recipe
from server.errors import http_errors
from server.logger import logger
from server.db import db


class RecipePlannerController(BaseCrudController):
    _model: RecipePlanner

    def handle_get_list(self, reqargs: dict, user_id: int) -> Response:
        try:
            query_planner_owner = self._model.query.filter(
                self._model.owner_user_id == user_id)

            query_planner_shared = self._model.query \
                .join(UserSharedRecipePlanner) \
                .filter(UserSharedRecipePlanner.user_id == user_id)

            query = query_planner_owner.union(query_planner_shared)

            return super().handle_get_list(
                reqargs=reqargs,
                query=query,
                redis_addition_key=f"uid:{user_id}"
            )
        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT


class RecipePlannerItemController(BaseCrudController):
    _model: RecipePlannerItem

    def handle_post_change_order(
            self,
            id: int,
            new_order_number: int
    ) -> Response:
        try:
            rp_item_obj: RecipePlannerItem = self._find_object_by_id(id)

            if new_order_number == rp_item_obj.order_number:
                return marshal(rp_item_obj, self._api_model)

            inc_number = 1
            if new_order_number > rp_item_obj.order_number:
                # new_order_number > area_obj.order_number
                updating_rp_items = self._model.query.filter(
                    and_(
                        self._model.rplanner_id == rp_item_obj.rplanner_id,
                        self._model.order_number > rp_item_obj.order_number,
                        self._model.order_number <= new_order_number
                    )
                ).all()
                inc_number = -1
            else:
                updating_rp_items = self._model.query.filter(
                    and_(
                        self._model.rplanner_id == rp_item_obj.rplanner_id,
                        self._model.order_number < rp_item_obj.order_number,
                        self._model.order_number >= new_order_number
                    )
                ).all()

            updating_rp_item: RecipePlannerItem
            for updating_rp_item in updating_rp_items:
                updating_rp_item.order_number += inc_number

            rp_item_obj.order_number = new_order_number

            db.session.commit()

            self._clear_cache()

            return marshal(rp_item_obj, self._api_model)

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_post(
            self,
            data: dict,
            unique_primarykey: Any = None
    ) -> Response:
        return super().handle_post(
            data=self._transform_date(data),
            unique_primarykey=unique_primarykey
        )

    def handle_patch(self, id: Any, data: dict) -> Response:
        return super().handle_patch(
            id=id,
            data=self._transform_date(data)
        )

    def _transform_date(self, data: dict) -> dict:
        try:
            date_value: date = parser.parse(data["date"]).date()
            data["date"] = date_value.strftime("%Y-%m-%d")
            return data
        except Exception:
            # if date is invalid, the validation will executed in super()
            return data


class UserSharedRecipePlannerController(BaseCrudController):
    pass


recipe_planner_controller = RecipePlannerController(
    model=RecipePlanner,
    api_model=recipe_planner_model,
    api_model_send=recipe_planner_model_send,
    unique_columns_together=["name", "owner_user_id"],
    read_only_fields=["owner_user_id"]
)


recipe_planner_item_controller = RecipePlannerItemController(
    model=RecipePlannerItem,
    api_model=recipe_planner_item_model,
    api_model_send=recipe_planner_item_model_send,
    read_only_fields=["rplanner_id", "recipe_id", "order_number"],
    foreign_key_columns=[
        (RecipePlanner, "rplanner_id"),
        (Recipe, "recipe_id")
    ],
    unique_columns_together=[
        "rplanner_id",
        "date",
        "order_number"
    ],
    clear_cache_models=[RecipePlanner]
)


user_shared_recipe_planner_controller = UserSharedRecipePlannerController(
    model=UserSharedRecipePlanner,
    api_model=user_shared_recipe_planner_model,
    api_model_send=user_shared_recipe_planner_model_send,
    foreign_key_columns=[
        (RecipePlanner, "rplanner_id")
        # (User, "user_id")
    ],
    read_only_fields=["rplanner_id", "user_id"],
    unique_columns_together=["rplanner_id", "user_id"],
    clear_cache_models=[RecipePlanner]
)
