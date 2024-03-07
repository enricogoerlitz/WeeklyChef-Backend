from flask import Response
from flask_sqlalchemy.model import Model

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
from server.api import api


class RecipePlannerController(BaseCrudController):
    _model: RecipePlanner

    def __init__(
            self,
            model: Model,
            api_model: api.model,  # type: ignore
            api_model_send: api.model = None,  # type: ignore
            unique_columns: list[str] = None,
            search_fields: list[str] = None,
            pagination_page_size: int = 20,
            use_caching: bool = True,
            clear_cache_models: list[Model] = None
    ) -> None:
        super().__init__(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            unique_columns=unique_columns,
            search_fields=search_fields,
            pagination_page_size=pagination_page_size,
            use_caching=use_caching,
            clear_cache_models=clear_cache_models
        )

    def handle_get_list(self, reqargs: dict, user_id: int) -> Response:
        # TODO: Add Try Catch
        # TODO: man sieht auch die, die mit einem geteilt sind!
        # return super().handle_get_list(reqargs=reqargs)
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


recipe_planner_controller = RecipePlannerController(
    model=RecipePlanner,
    api_model=recipe_planner_model,
    api_model_send=recipe_planner_model_send,
    use_caching=True
)


recipe_planner_item_controller = BaseCrudController(
    model=RecipePlannerItem,
    api_model=recipe_planner_item_model,
    api_model_send=recipe_planner_item_model_send,
    use_caching=True,
    clear_cache_models=[RecipePlanner]
)


user_shared_recipe_planner_controller = BaseCrudController(
    model=UserSharedRecipePlanner,
    api_model=user_shared_recipe_planner_model,
    api_model_send=user_shared_recipe_planner_model_send,
    use_caching=True,
    clear_cache_models=[RecipePlanner]
)
