from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from server.utils import swagger as sui
from server.core.controller import crud_controller as CRUDController
from server.core.models.api_models.utils import error_model
from server.core.permissions.general import IsAdminOrStaff
from server.core.models.api_models.recipe import (
    category_model, category_model_send
)
from server.core.models.db_models import Category
from server.services.recipe.controller.category import category_controller


ns = Namespace(
    name="Category",
    description=__name__,
    path="/api/v1/category"
)


@ns.route("/")
class CategoryListAPI(Resource):

    @ns.response(code=200, model=[category_model], description=sui.desc_list(ns.name))          # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        return category_controller.handle_get_list(request.args)
        return CRUDController.handle_get_list(
            model=Category,
            api_model=category_model,
            reqargs=request.args,
            search_fields=["name"]
        )

    @ns.expect(category_model_send)
    @ns.response(code=201, model=category_model, description=sui.desc_added(ns.name))           # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        return category_controller.handle_post(
            data=request.get_json()
        )
        return CRUDController.handle_post(
            model=Category,
            api_model=category_model,
            api_model_send=category_model_send,
            data=request.get_json(),
            unique_columns=["name"]
        )


@ns.route("/<int:id>")
class CategoryAPI(Resource):

    @ns.response(code=200, model=category_model, description=sui.desc_get(ns.name))             # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return category_controller.handle_get(id)
        return CRUDController.handle_get(Category, category_model, id)

    @ns.expect(category_model_send)
    @ns.response(code=200, model=category_model, description=sui.desc_update(ns.name))          # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def patch(self, id):
        return category_controller.handle_patch(
            id=id,
            data=request.get_json()
        )
        return CRUDController.handle_patch(
            model=Category,
            api_model=category_model,
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def delete(self, id):
        return category_controller.handle_delete(id)
        return CRUDController.handle_delete(Category, id)
