from sqlalchemy import or_
from flask import Response
from flask_sqlalchemy.model import Model
from flask_sqlalchemy.query import Query

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
from server.core.models.db_models.recipe.tag import Tag
from server.core.models.db_models.recipe.ingredient import Ingredient
from server.core.models.db_models.recipe.category import Category


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
        search = reqargs.get("search")
        difficulty_search = reqargs.get("difficulty")
        query: Query = self._model.query

        if search is not None:
            search_str = f"%{search}%"

            query_recipe = query.filter(
                or_(
                    Recipe.name.like(search_str),
                    Recipe.search_description.like(search_str),
                    Recipe.preperation_description.like(search_str)
                )
            )

            query_tag_search = query \
                .join(RecipeTagComposite) \
                .join(Tag) \
                .filter(Tag.name.like(search_str))

            query_ingredient_search = query \
                .join(RecipeIngredient) \
                .join(Ingredient) \
                .filter(Ingredient.name.like(search_str))

            query_category_search = query.join(Category).filter(
                Category.name.like(search_str)
            )

            query = query_recipe.union(query_tag_search) \
                                .union(query_ingredient_search) \
                                .union(query_category_search)

        if difficulty_search is not None:
            query = query.filter(Recipe.difficulty == difficulty_search)

        return super().handle_get_list(reqargs, query=query)


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
