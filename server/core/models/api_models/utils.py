""""""
from flask_restx import fields
from api import api


base_name_model_fields = {
    "id": fields.Integer,
    "name": fields.String
}


base_name_model_fields_send = {
    "name": fields.String
}


error_model = api.model("ErrorModel", {
    "msg": fields.String
})
