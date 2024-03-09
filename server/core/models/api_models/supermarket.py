from flask_restx import fields

from server.api import api


# SUPERMARKET MODELS

util_area_ingredient_model = api.model("utils", {
    "ingredient_price": fields.Float,
    "ingredient": fields.Nested(
        api.model("utils", {
            "id": fields.Integer,
            "displayname": fields.String,
            "default_price": fields.Float
        })
    ),
})


util_sam_model = api.model("utils", {
    "id": fields.Integer,
    "name": fields.String,
    "order_number": fields.Integer,
    "ingredients": fields.List(
        fields.Nested(util_area_ingredient_model)
    )
})


supermarket_area_model = api.model("SupermarketAreaModel", {
    "id": fields.Integer,
    "name": fields.String,
    "order_number": fields.Integer,
    "supermarket_id": fields.Integer,
    "ingredients": fields.List(
        fields.Nested(util_area_ingredient_model)
    ),
})


supermarket_area_model_send = api.model("SupermarketAreaModelSend", {
    "name": fields.String,
    "order_number": fields.Integer
})


supermarket_area_ingredinet_model = api.model("SupermarketAreaIngredientModel", {  # noqa
    "sarea_id": fields.Integer,
    "ingredient_id": fields.Integer,
    "ingredient_price": fields.Float
})


supermarket_area_ingredinet_model_send = api.model("SupermarketAreaIngredientModelSend", {  # noqa
    "ingredient_price": fields.Float
})


supermarket_model_detail = api.model("SupermarketModel", {
    "id": fields.Integer,
    "name": fields.String,
    "street": fields.String,
    "postcode": fields.String,
    "district": fields.String,
    "owner_user_id": fields.Integer,
    "areas": fields.List(fields.Nested(supermarket_area_model))
})


supermarket_model = api.model("SupermarketModel", {
    "id": fields.Integer,
    "name": fields.String,
    "street": fields.String,
    "postcode": fields.String,
    "district": fields.String,
    "owner_user_id": fields.Integer
})


supermarket_model_detail = api.model("SupermarketModelDetail", {
    "id": fields.Integer,
    "name": fields.String,
    "street": fields.String,
    "postcode": fields.String,
    "district": fields.String,
    "owner_user_id": fields.Integer,
    "areas": fields.List(
        fields.Nested(util_sam_model)
    )
})

supermarket_model_send = api.model("SupermarketModelSend", {
    "name": fields.String,
    "street": fields.String,
    "postcode": fields.String,
    "district": fields.String
})


supermarket_user_edit_model = api.model("SupermarketUserEditModel", {
    "supermarket_id": fields.Integer,
    "user_id": fields.Integer
})
