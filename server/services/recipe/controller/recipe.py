from flask import Response
from flask_sqlalchemy.model import Model

from server.api import api
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.recipe.recipe import (
    Recipe, RecipeIngredient, RecipeTagComposite
)
from server.core.models.api_models.recipe import (
    recipe_ingredient_model,
    recipe_ingredient_model_send,
    recipe_model,
    recipe_model_send,
    recipe_tag_model
)


class RecipeController(BaseCrudController):

    def __init__(
            self,
            model: Model,
            api_model: api.model,  # type: ignore
            api_model_send: api.model = None,  # type: ignore
            unique_columns: list[str] = None,
            search_fields: list[str] = None,
            pagination_page_size: int = 20,
            use_redis: bool = True
    ) -> None:
        super().__init__(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            unique_columns=unique_columns,
            search_fields=search_fields,
            pagination_page_size=pagination_page_size,
            use_redis=use_redis
        )

    def handle_get_list(self, reqargs: dict) -> Response:
        # OVERRIDE
        # HIER zusätzlich suche nach TAG und INGREDIENT einbauen!
        # model_query = ...filter() -> an handle_get_list query übergeben!
        return super().handle_get_list(reqargs)


recipe_controller = RecipeController(
    model=Recipe,
    api_model=recipe_model,
    api_model_send=recipe_model_send,
    unique_columns=["name"],
    search_fields=[
        "name",
        "search_description",
        "preperation_description"
    ],
    pagination_page_size=20,
    use_redis=False
)


recipe_ingredient_controller = BaseCrudController(
    model=RecipeIngredient,
    api_model=recipe_ingredient_model,
    api_model_send=recipe_ingredient_model_send,
    unique_columns=None,
    search_fields=None,
    pagination_page_size=20,
    use_redis=True
)


recipe_tag_controller = BaseCrudController(
    model=RecipeTagComposite,
    api_model=recipe_tag_model,
    api_model_send=recipe_tag_model,
    unique_columns=None,
    search_fields=None,
    pagination_page_size=20,
    use_redis=True
)
