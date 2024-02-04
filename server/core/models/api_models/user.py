from flask_restx import fields

from api import api


role_model = api.model("RoleModel", {
    "id": fields.Integer,
    "name": fields.String
})


user_model = api.model("UserModel", {
    "id": fields.Integer,
    "email": fields.String,
    "username": fields.String,
    "roles": fields.List(fields.Nested(role_model))
})
