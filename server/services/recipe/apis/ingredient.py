"""
Ingredient Routes
"""

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from utils import swagger as sui
from core.controller import crud_controller
from core.models.api_models.utils import error_model
from core.permissions.general import IsAdminOrStaff
from core.models.api_models.recipe import (
    ingredient_model, ingredient_model_send
)
from core.models.db_models import Ingredient


ns = Namespace(
    name="Ingredient",
    description=__name__,
    path="/api/v1/ingredient"
)


@ns.route("/")
class IngredientListAPI(Resource):

    @ns.response(code=200, model=[ingredient_model], description=sui.desc_list(ns.name))            # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    def get(self):
        return crud_controller.handle_get_list(
            model=Ingredient,
            api_model=ingredient_model
        )

    @ns.expect(ingredient_model_send)
    @ns.response(code=200, model=ingredient_model, description=sui.desc_added(ns.name))             # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))               # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        return crud_controller.handle_post(
            model=Ingredient,
            api_model=ingredient_model,
            api_model_send=ingredient_model_send,
            data=request.get_json(),
            unique_columns=["name"]
        )


@ns.route("/<int:id>")
class IngredientAPI(Resource):

    @ns.response(code=200, model=ingredient_model, description=sui.desc_get(ns.name))               # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    def get(self, id):
        return crud_controller.handle_get(Ingredient, ingredient_model, id)

    @ns.expect(ingredient_model_send)
    @ns.response(code=200, model=ingredient_model, description=sui.desc_update(ns.name))            # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsAdminOrStaff
    def put(self, id):
        return crud_controller.handle_update(
            model=Ingredient,
            api_model=ingredient_model,
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsAdminOrStaff
    def delete(self, id):
        return crud_controller.handle_delete(Ingredient, id)
