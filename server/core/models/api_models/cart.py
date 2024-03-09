from flask_restx import fields
from server.api import api
from server.core.models.api_models.recipe import ingredient_model, recipe_model


cart_item_model = api.model("CartItemModel", {
    "id": fields.Integer,
    "cart_id": fields.Integer,
    "recipe_id": fields.Integer,
    "ingredient_id": fields.Integer,
    "quantity": fields.Integer,
    "is_done": fields.Boolean,
    "recipe": fields.Nested(recipe_model),  # TODO: only id and name!
    "ingredient": fields.Nested(ingredient_model)
})

cart_item_model_send = api.model("CartItemModelSend", {
    "recipe_id": fields.Integer,
    "ingredient_id": fields.Integer,
    "quantity": fields.Integer,
    "is_done": fields.Boolean
})


cart_model = api.model("CartModel", {
    "id": fields.Integer,
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_active": fields.Boolean,
    "items": fields.List(fields.Nested(cart_item_model))
})

cart_model_send = api.model("CartModelSend", {
    "name": fields.String,
    "is_active": fields.Boolean
})


user_shared_cart_model = api.model("UserSharedCartModel", {
    "cart_id": fields.Integer,
    "user_id": fields.Integer
})
