from server.api import api
from server.core.models.api_models.utils import (
    base_name_model_fields,
    base_name_model_fields_send
)


# API MODELS

unit_model = api.model(
    "UnitModel",
    base_name_model_fields
)

unit_model_send = api.model(
    "UnitModelSend",
    base_name_model_fields_send
)
