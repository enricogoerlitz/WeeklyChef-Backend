from flask import Response

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
from server.core.models.db_models.user.user import User
from server.core.models.db_models.recipe.recipe import Recipe
from server.errors import http_errors
from server.logger import logger


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
    pass


class UserSharedRecipePlannerController(BaseCrudController):
    pass


recipe_planner_controller = RecipePlannerController(
    model=RecipePlanner,
    api_model=recipe_planner_model,
    api_model_send=recipe_planner_model_send,
    unique_columns_together=["name", "owner_user_id"],
    foreign_key_columns=[
        (User, "owner_user_id")
    ],
    read_only_fields=["owner_user_id"],
    use_caching=True
)


recipe_planner_item_controller = RecipePlannerItemController(
    model=RecipePlannerItem,
    api_model=recipe_planner_item_model,
    api_model_send=recipe_planner_item_model_send,
    read_only_fields=["rplanner_id", "recipe_id"],
    foreign_key_columns=[
        (RecipePlanner, "rplanner_id"),
        (Recipe, "recipe_id")
    ],
    unique_columns_together=[
        "rplanner_id",
        "date",  # TODO: date auf 0 setzen (mm,ss etc)
        "order_number"
    ],
    use_caching=True,
    clear_cache_models=[RecipePlanner]
)


user_shared_recipe_planner_controller = UserSharedRecipePlannerController(
    model=UserSharedRecipePlanner,
    api_model=user_shared_recipe_planner_model,
    api_model_send=user_shared_recipe_planner_model_send,
    foreign_key_columns=[
        (RecipePlanner, "rplanner_id"),
        (User, "user_id")
    ],
    read_only_fields=["rplanner_id", "user_id"],
    unique_columns_together=["rplanner_id", "user_id"],
    use_caching=True,
    clear_cache_models=[RecipePlanner]
)
