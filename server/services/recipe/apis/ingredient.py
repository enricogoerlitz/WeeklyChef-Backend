from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.permissions.general import IsAdminOrStaff
from server.core.models.api_models.ingredient import (
    ingredient_model, qpp_ingredient_model,
    ingredient_model_send)
from server.services.recipe.controller.ingredient import ingredient_controller


ns = Namespace(
    name="Ingredient",
    description=__name__,
    path="/api/v1/ingredient"
)


@ns.route("/")
class IngredientListAPI(Resource):

    @ns.expect(qpp_ingredient_model)
    @ns.response(code=200, model=[ingredient_model], description=sui.desc_list(ns.name))            # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    def get(self):
        return ingredient_controller.handle_get_list(request.args)

    @ns.expect(ingredient_model_send)
    @ns.response(code=201, model=ingredient_model, description=sui.desc_added(ns.name))             # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))               # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                  # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    def post(self):
        return ingredient_controller.handle_post(
            data=request.get_json()
        )


@ns.route("/<int:id>")
class IngredientAPI(Resource):

    @ns.response(code=200, model=ingredient_model, description=sui.desc_get(ns.name))               # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))               # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    def get(self, id):
        return ingredient_controller.handle_get(id)

    @ns.expect(ingredient_model_send)
    @ns.response(code=200, model=ingredient_model, description=sui.desc_update(ns.name))            # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))               # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                  # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsAdminOrStaff
    def patch(self, id):
        return ingredient_controller.handle_patch(
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))               # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsAdminOrStaff
    def delete(self, id):
        return ingredient_controller.handle_delete(id)
