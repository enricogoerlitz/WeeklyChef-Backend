""""""
from flask_restx import fields
from api import api


error_model = api.model("ErrorModel", {
    "msg": fields.String
})
