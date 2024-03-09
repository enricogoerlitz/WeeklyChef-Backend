from flask_restx import fields, reqparse

from server.api import api
from server.core.enums import difficulty
from server.core.models.api_models.utils import (
    base_name_model_fields,
    base_name_model_fields_send,
    reqparse_add_queryparams_doc
)
from server.core.models.api_models.utils import acl_model


# GET QUERY MODELS

#   RECIPE GET LIST MODEL

recipe_reqparser = reqparse.RequestParser()
recipe_reqparser.add_argument(
    "difficulty",
    type=str,
    choices=list(difficulty.ALLOWED_DIFFICULTIES),
    location="args"
)
recipe_model_get_list = reqparse_add_queryparams_doc(
    parser=recipe_reqparser,
    add_search_utils=True,
    add_pagination=True,
    query_params=[
        ("search", str),
        ("name", str),
        ("search_description", str),
        ("preparation_description", str)
    ]
)

#   RECIPE RATING GET MODEL
recipe_rating_model_get = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search_utils=False,
    add_pagination=False,
    query_params=[
        ("user_id", int)
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
    "category_id": fields.Integer
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

recipe_image_model = api.model("RecipeImageModel", {
    "id": fields.Integer
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
    "tags": fields.List(fields.Nested(tag_model)),
    "images": fields.List(fields.Nested(recipe_image_model))
})


recipe_image_model = api.model("RecipeImageCompositeModel", {
    "recipe_id": fields.Integer,
    "image_id": fields.Integer
})

recipe_rating_model = api.model("RecipeRatingModel", {
    "user_id": fields.Integer,
    "recipe_id": fields.Integer,
    "rating": fields.Float
})

recipe_rating_model_agg = api.model("RecipeRatingModelAggregation", {
    "rating_avg": fields.Float,
    "rating_count": fields.Integer
})

recipe_rating_model_send = api.model("RecipeDatingModelSend", {
    "rating": fields.Float,
})


# COLLECTION MODELS


collection_recipe_model = api.model("utils", {
    "id": fields.Integer,
    "name": fields.String,
    "preperation_description": fields.String,
    "difficulty": fields.String,
    "person_count": fields.Integer,
    "preperation_time_minutes": fields.Integer,
    "search_description": fields.String,
    "creator_user_id": fields.Integer,
    "category": fields.Nested(category_model),
    "tags": fields.List(fields.Nested(tag_model)),
    "images": fields.List(fields.Nested(recipe_image_model))
})


collection_model = api.model("CollectionModel", {
    "id": fields.Integer,
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_default": fields.Boolean,
    "recipes": fields.List(
        fields.Nested(api.model("utils", {
            "recipe": fields.Nested(collection_recipe_model)
        }))
    ),
    "acl": fields.List(fields.Nested(acl_model))
})

collection_model_send = api.model("CollectionModelSend", {
    "name": fields.String,
    "is_default": fields.Boolean
})

collection_recipe_model = api.model("CollectionRecipeModel", {
    "collection_id": fields.Integer,
    "recipe_id": fields.Integer
})

user_shared_collection_model = api.model("CollectionUserModel", {
    "collection_id": fields.Integer,
    "user_id": fields.Integer,
    "can_edit": fields.Boolean
})

user_shared_collection_model_send = api.model("CollectionUserModelSend", {
    "can_edit": fields.Boolean
})
