from datetime import date

from flask_restx import fields, reqparse

from server.api import api
from server.core.models.api_models.category import category_model
from server.core.models.api_models.utils import (
    acl_model, reqparse_add_queryparams_doc
)


# GET QUERY MODELS

qpp_recipe_planner_model = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search_utils=True,
    add_pagination=True,
    query_params=[
        ("name", str)
    ]
)

qpp_recipe_planner_item_model = reqparse_add_queryparams_doc(
    parser=reqparse.RequestParser(),
    add_search_utils=False,
    add_pagination=False,
    query_params=[
        ("date_of_week", date)
    ]
)


# API MODELS

u_recipe_planner_item_recipe_model = api.model("utils", {
    "id": fields.Integer,
    "name": fields.String,
    "category": fields.Nested(category_model)
})

recipe_planner_item_model = api.model("RecipePlannerItemModel", {
    "id": fields.Integer,
    "rplanner_id": fields.Integer,
    "date": fields.Date,
    "label": fields.String,
    "order_number": fields.Integer,
    "planned_recipe_person_count": fields.Integer,
    "recipe": fields.Nested(u_recipe_planner_item_recipe_model)
})

recipe_planner_item_model_send = api.model("RecipePlannerItemModelSend", {
    "rplanner_id": fields.Integer,
    "recipe_id": fields.Integer,
    "date": fields.Date,
    "label": fields.String,
    "order_number": fields.Integer,
    "planned_recipe_person_count": fields.Integer,
})

recipe_planner_model_detail = api.model("RecipePlannerModel", {
    "id": fields.Integer,
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_active": fields.Boolean,
    "acl": fields.List(fields.Nested(acl_model))
})

recipe_planner_model = api.model("RecipePlannerModel", {
    "id": fields.Integer,
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_active": fields.Boolean
})

recipe_planner_model_send = api.model("RecipePlannerModelSend", {
    "name": fields.String,
    "is_active": fields.Boolean
})

user_shared_recipe_planner_model = api.model("UserSharedRecipePlannerModel", {
    "rplanner_id": fields.Integer,
    "user_id": fields.Integer,
    "can_edit": fields.Boolean
})

user_shared_recipe_planner_model_send = api.model("UserSharedRecipePlannerModelSend", {  # noqa
    "can_edit": fields.Boolean
})
