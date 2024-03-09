from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.tag import Tag
from server.core.models.api_models.recipe import (
    tag_model, tag_model_send
)
from server.core.models.db_models.recipe import Recipe
from server.core.models.db_models.collection import Collection


class TagController(BaseCrudController):
    pass


tag_controller = TagController(
    model=Tag,
    api_model=tag_model,
    api_model_send=tag_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    clear_cache_models=[Recipe, Collection]
)
