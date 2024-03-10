from server.core.controller.crud_controller import BaseCrudController
from server.core.models.api_models.ingredient import (
    ingredient_model, ingredient_model_send
)
from server.core.models.db_models.recipe import Recipe
from server.core.models.db_models.planner import RecipePlanner
from server.core.models.db_models.ingredient import Ingredient
from server.core.models.db_models.cart import Cart
from server.core.models.db_models.supermarket import Supermarket


class IngredientController(BaseCrudController):
    pass


ingredient_controller = IngredientController(
    model=Ingredient,
    api_model=ingredient_model,
    api_model_send=ingredient_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    clear_cache_models=[Recipe, RecipePlanner, Cart, Supermarket],
    use_caching=True
)
