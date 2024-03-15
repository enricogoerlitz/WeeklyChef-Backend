from server.api import api
from server.core.models.api_models.utils import (
    base_name_model_fields, base_name_model_fields_send
)

# API MODELS

category_model = api.model(
    "CategoryModel",
    base_name_model_fields
)

category_model_send = api.model(
    "CategoryModelSend",
    base_name_model_fields_send
)
