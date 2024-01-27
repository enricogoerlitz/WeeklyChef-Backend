"""
Auth models
"""

from flask_restx import fields

from config import api

register_model = api.model("RegisterModel", {
    "email": fields.String,
    "username": fields.String,
    "password": fields.String
})

login_model = api.model("LoginModel", {
    "username": fields.String,
    "password": fields.String
})

jwt_model = api.model("JWTModel", {
    "access_token": fields.String,
    "refresh_token": fields.String
})
