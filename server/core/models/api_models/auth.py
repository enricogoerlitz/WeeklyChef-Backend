from flask_restx import fields

from config import api

register_model_send = api.model("RegisterModelSend", {
    "email": fields.String,
    "username": fields.String,
    "password": fields.String
})

login_model_send = api.model("LoginModelSend", {
    "username": fields.String,
    "password": fields.String
})

jwt_model = api.model("JWTModel", {
    "access_token": fields.String,
    "refresh_token": fields.String
})
