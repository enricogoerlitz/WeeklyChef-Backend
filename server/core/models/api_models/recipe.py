from flask_restx import fields, reqparse

from server.api import api
from server.core.models.api_models.utils import (
    base_name_model_fields,
    base_name_model_fields_send,
    reqparse_add_queryparams_doc
)


# GET-LIST MODELS

#   RECIPE GET LIST MODEL

recipe_model_get_list = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search=True,
    add_pagination=True,
    query_params=[
        ("name", str),
        ("search_description", str),
        ("preparation_description", str)
    ]
)


# UNIT MODELS

unit_model = api.model(
    "UnitModel", base_name_model_fields)

unit_model_send = api.model(
    "UnitModelSend", base_name_model_fields_send)


# CATEGORY MODELS

category_model = api.model(
    "CategoryModel", base_name_model_fields)

category_model_send = api.model(
    "CategoryModelSend", base_name_model_fields_send)


# TAG MODELS

tag_model = api.model(
    "TagModel", base_name_model_fields)

tag_model_send = api.model(
    "TagModelSend", base_name_model_fields_send)


# INGREDIENT MODELS

ingredient_model = api.model("IngredientModel", {
    "id": fields.Integer,
    "name": fields.String,
    "displayname": fields.String,
    "default_price": fields.Float,
    "quantity_per_unit": fields.Float,
    "is_spices": fields.Boolean,
    "search_description": fields.String,
    "unit_id": fields.Integer,
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


# RECIPE MODELS

recipe_model_send = api.model("RecipeModelSend", {
    "name": fields.String,
    "preperation_description": fields.String,
    "difficulty": fields.String,
    "person_count": fields.Integer,
    "preperation_time_minutes": fields.Integer,
    "search_description": fields.String,
    "category_id": fields.Integer,
    "creator_user_id": fields.Integer
})

recipe_tag_model = api.model("RecipeTagModel", {
    "recipe_id": fields.Integer,
    "tag_id": fields.Integer
})

recipe_ingredient_model = api.model("RecipeIngredientModel", {
    "recipe_id": fields.Integer,
    "ingredient_id": fields.Integer,
    "quantity": fields.Float
})

recipe_ingredient_model_joined = api.model("RecipeIngredientModelJoined", {
    "quantity": fields.Float,
    "ingredient": fields.Nested(ingredient_model)
})

recipe_ingredient_model_send = api.model("RecipeIngredientModelSend", {
    "quantity": fields.Float
})

recipe_model = api.model("RecipeModel", {
    "id": fields.Integer,
    "name": fields.String,
    "preperation_description": fields.String,
    "difficulty": fields.String,
    "person_count": fields.Integer,
    "preperation_time_minutes": fields.Integer,
    "search_description": fields.String,
    "creator_user_id": fields.Integer,
    "category": fields.Nested(category_model),
    "ingredients": fields.List(fields.Nested(recipe_ingredient_model_joined)),
    "tags": fields.List(fields.Nested(tag_model))
})


# COLLECTION MODELS

collection_model = api.model("Collection", {
    "id": fields.Integer,
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_default": fields.Boolean
})

collection_model_send = api.model("CollectionSend", {
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_default": fields.Boolean
})

collection_recipe_model = api.model("CollectionRecipeModel", {
    "collection_id": fields.Integer,
    "recipe_id": fields.Integer
})

collection_user_model = api.model("CollectionUserModel", {
    "collection_id": fields.Integer,
    "user_id": fields.Integer,
    "can_edit": fields.Boolean
})

collection_user_model_send = api.model("CollectionUserModelSend", {
    "can_edit": fields.Boolean
})
