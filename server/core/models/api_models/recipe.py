from flask_restx import fields, reqparse

from server.api import api
from server.core.enums import difficulty
from server.core.models.api_models.utils import (
    reqparse_add_queryparams_doc
)
from server.core.models.api_models.ingredient import ingredient_model
from server.core.models.api_models.category import category_model
from server.core.models.api_models.tag import tag_model


# GET QUERY MODELS

recipe_reqparser = reqparse.RequestParser()
recipe_reqparser.add_argument(
    "difficulty",
    type=str,
    choices=list(difficulty.ALLOWED_DIFFICULTIES),
    location="args"
)
qpp_recipe_model = reqparse_add_queryparams_doc(
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

qpp_recipe_rating_model = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search_utils=False,
    add_pagination=False,
    query_params=[
        ("user_id", int)
    ]
)


# API MODELS

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
    "category_id": fields.Integer
})

recipe_model_detail = api.model("RecipeModel", {
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
