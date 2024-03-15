from flask_restx import fields

from server.api import api


# API MODELS

role_model = api.model("RoleModel", {
    "id": fields.Integer,
    "name": fields.String
})


user_model_public = api.model("UserModel", {
    "id": fields.Integer,
    "username": fields.String,
})


user_model_admin = api.model("UserModel", {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String,
    "roles": fields.List(fields.Nested(role_model))
})
