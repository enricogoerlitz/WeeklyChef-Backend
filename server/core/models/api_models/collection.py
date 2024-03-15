from flask_restx import reqparse, fields

from server.core.models.api_models.utils import (
    acl_model, reqparse_add_queryparams_doc
)
from server.api import api
from server.core.models.api_models.category import category_model
from server.core.models.api_models.recipe import recipe_image_model
from server.core.models.api_models.tag import tag_model


# GET QUERY MODELS

qpp_collection_model = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search_utils=True,
    add_pagination=False,
    query_params=[
        ("name", str)
    ]
)


# API MODELS

u_collection_recipe_model = api.model("utils", {
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

collection_model = api.model("CollectionModelDetail", {
    "id": fields.Integer,
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_default": fields.Boolean,
    "recipes": fields.List(fields.Nested(u_collection_recipe_model)),
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
