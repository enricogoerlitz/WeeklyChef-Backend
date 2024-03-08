from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models import Unit
from server.core.models.api_models.recipe import (
    unit_model, unit_model_send,
)


class UnitController(BaseCrudController):
    pass


unit_controller = UnitController(
    model=Unit,
    api_model=unit_model,
    api_model_send=unit_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    pagination_page_size=20,
    use_caching=True
)
