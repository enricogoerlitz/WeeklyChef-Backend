""""""

from flask import request
from flask_restx import Resource, Namespace

from db import db
from api import api
from server.core.controller import crud_controller
from core.models.api_models.utils import error_model


class BaseListAPI(Resource):
    ns: Namespace
    db_model: db.Model
    api_model: api.model
    err_model: api.model = error_model

    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.get = self.ns.response(
            code=200,
            model=[self.api_model],
            description="List of category models"
        )(lambda res: res)
        self.get = self.ns.response(
            code=500,
            model=self.err_model,
            description="Unexpected error"
        )(lambda: self.handle_get())

    # @ns.response(code=200, model=[api_model], description="List of category models")  # noqa
    # @ns.response(code=500, model=err_model, description="Unexpected error")  # noqa
    def handle_get(self):
        return crud_controller.handle_get_list(self.db_model, self.api_model)

    # @ns.response(code=200, model=api_model, description="Add category")  # noqa
    # @ns.response(code=500, model=err_model, description="Unexpected error")  # noqa
    # def post(self):
    #     return crud.handle_post(self.db_model, self.api_model, request.get_json())  # noqa
