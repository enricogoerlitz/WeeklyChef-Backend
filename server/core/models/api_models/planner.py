from flask_restx import fields
from server.api import api
from server.core.models.api_models.recipe import recipe_model


recipe_planner_item_model = api.model("RecipePlannerItemModel", {
    "id": fields.Integer,
    "rplanner_id": fields.Integer,
    "recipe_id": fields.Integer,
    "date": fields.DateTime,
    "label": fields.String,
    "order_number": fields.Integer,
    "planned_recipe_person_count": fields.Integer,
    "recipe": fields.Nested(recipe_model)
})


recipe_planner_item_model_send = api.model("RecipePlannerItemModelSend", {
    "rplanner_id": fields.Integer,
    "recipe_id": fields.Integer,
    "date": fields.DateTime,
    "label": fields.String,
    "order_number": fields.Integer,
    "planned_recipe_person_count": fields.Integer,
})


recipe_planner_model = api.model("RecipePlannerModel", {
    "id": fields.Integer,
    "name": fields.String,
    "owner_user_id": fields.Integer,
    "is_active": fields.Boolean,
    "items": fields.List(fields.Nested(recipe_planner_item_model))
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
