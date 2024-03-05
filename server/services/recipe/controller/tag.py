from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.recipe.tag import Tag
from server.core.models.api_models.recipe import (
    tag_model, tag_model_send
)


tag_controller = BaseCrudController(
    model=Tag,
    api_model=tag_model,
    api_model_send=tag_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    pagination_page_size=20,
    use_redis=True
)
