from server.core.models.db_models.recipe.collection import (
    Collection, CollectionRecipeComposite
)
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.api_models.recipe import (
    collection_model,
    collection_model_send,
    collection_recipe_model
)


collection_controller = BaseCrudController(
    model=Collection,
    api_model=collection_model,
    api_model_send=collection_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    pagination_page_size=20,
    use_redis=True
)

collection_recipe_controller = BaseCrudController(
    model=CollectionRecipeComposite,
    api_model=collection_recipe_model,
    api_model_send=collection_recipe_model,
    unique_columns=None,
    search_fields=None,
    pagination_page_size=20,
    use_redis=True
)
