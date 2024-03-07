from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.recipe.collection import Collection
from server.core.models.api_models.recipe import (
    ingredient_model, ingredient_model_send
)


ingredient_controller = BaseCrudController(
    model=Collection,
    api_model=ingredient_model,
    api_model_send=ingredient_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    pagination_page_size=20,
    use_caching=True
)
