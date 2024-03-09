from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.recipe.category import Category
from server.core.models.api_models.recipe import (
    category_model, category_model_send
)
from server.core.models.db_models.recipe.recipe import Recipe


class CategoryController(BaseCrudController):
    pass


category_controller = CategoryController(
    model=Category,
    api_model=category_model,
    api_model_send=category_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    clear_cache_models=[Recipe]
)
