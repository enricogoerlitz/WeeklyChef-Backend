"""
Unit Routes
"""

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from utils import swagger as sui
from core.controller import crud_controller
from core.models.api_models.utils import error_model
from core.permissions.general import IsAdminOrStaff
from core.models.api_models.recipe import (
    unit_model, unit_model_send
)
from core.models.db_models import Unit


ns = Namespace(
    name="Unit",
    description=__name__,
    path="/api/v1/unit"
)


@ns.route("/")
class UnitListAPI(Resource):

    @ns.response(code=200, model=[unit_model], description=sui.desc_list(ns.name))              # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        return crud_controller.handle_get_list(
            model=Unit,
            api_model=unit_model
        )

    @ns.expect(unit_model_send)
    @ns.response(code=201, model=unit_model, description=sui.desc_added(ns.name))               # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        return crud_controller.handle_post(
            model=Unit,
            api_model=unit_model,
            api_model_send=unit_model_send,
            data=request.get_json(),
            unique_columns=["name"]
        )


@ns.route("/<int:id>")
class UnitAPI(Resource):

    @ns.response(code=200, model=unit_model, description=sui.desc_get(ns.name))                 # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return crud_controller.handle_get(Unit, unit_model, id)

    @ns.expect(unit_model_send)
    @ns.response(code=200, model=unit_model, description=sui.desc_update(ns.name))              # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def put(self, id):
        return crud_controller.handle_update(
            model=Unit,
            api_model=unit_model,
            id=id,
            data=request.get_json()
        )

    @ns.response(code=200, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def delete(self, id):
        return crud_controller.handle_delete(Unit, id)
