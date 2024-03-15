from flask_restx import reqparse

from server.core.models.api_models.utils import (
    base_name_model_fields,
    base_name_model_fields_send, reqparse_add_queryparams_doc
)
from server.api import api


# GET QUERY MODELS

qpp_tag_model = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search_utils=True,
    add_pagination=True,
    query_params=[
        ("name", str)
    ]
)

# API MODELS

tag_model = api.model(
    "TagModel",
    base_name_model_fields
)

tag_model_send = api.model(
    "TagModelSend",
    base_name_model_fields_send
)
