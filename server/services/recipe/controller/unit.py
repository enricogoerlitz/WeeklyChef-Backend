from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.unit import Unit
from server.core.models.api_models.unit import (
    unit_model, unit_model_send,
)
from server.core.models.db_models.ingredient import Ingredient
from server.core.models.db_models.recipe import Recipe
from server.core.models.db_models.planner import RecipePlanner


class UnitController(BaseCrudController):
    pass


unit_controller = UnitController(
    model=Unit,
    api_model=unit_model,
    api_model_send=unit_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    clear_cache_models=[Ingredient, Recipe, RecipePlanner],
    use_caching=False
)
