from flask_restx import reqparse, fields
from server.core.models.api_models.utils import reqparse_add_queryparams_doc
from server.api import api
from server.core.models.api_models.unit import unit_model


# GET QUERY MODELS

qpp_ingredient_model = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search_utils=True,
    add_pagination=True,
    query_params=[
        ("name", str)
    ]
)


# API MODELS

ingredient_model = api.model("IngredientModel", {
    "id": fields.Integer,
    "name": fields.String,
    "displayname": fields.String,
    "default_price": fields.Float,
    "quantity_per_unit": fields.Float,
    "is_spices": fields.Boolean,
    "search_description": fields.String,
    "unit": fields.Nested(unit_model)
})

ingredient_model_send = api.model("IngredientModelSend", {
    "name": fields.String,
    "displayname": fields.String,
    "default_price": fields.Float,
    "quantity_per_unit": fields.Float,
    "is_spices": fields.Boolean,
    "search_description": fields.String,
    "unit_id": fields.Integer
})
