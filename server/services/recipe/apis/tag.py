from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.permissions.general import IsAdminOrStaff
from server.core.models.api_models.tag import (
    tag_model, qpp_tag_model, tag_model_send
)
from server.services.recipe.controller.tag import tag_controller


ns = Namespace(
    name="Tag",
    description=__name__,
    path="/api/v1/tag"
)


@ns.route("/")
class TagListAPI(Resource):

    @ns.expect(qpp_tag_model)
    @ns.response(code=200, model=[tag_model], description=sui.desc_list(ns.name))           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                  # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                   # noqa
    @jwt_required()
    def get(self):
        return tag_controller.handle_get_list(request.args)

    @ns.expect(tag_model_send)
    @ns.response(code=201, model=tag_model, description=sui.desc_added(ns.name))            # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                  # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))       # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                   # noqa
    @jwt_required()
    def post(self):
        return tag_controller.handle_post(
            data=request.get_json()
        )


@ns.route("/<int:id>")
class TagAPI(Resource):

    @ns.response(code=200, model=tag_model, description=sui.desc_get(ns.name))              # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                   # noqa
    @jwt_required()
    def get(self, id):
        return tag_controller.handle_get(id)

    @ns.expect(tag_model_send)
    @ns.response(code=200, model=tag_model, description=sui.desc_update(ns.name))           # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))       # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                   # noqa
    @jwt_required()
    @IsAdminOrStaff
    def patch(self, id):
        return tag_controller.handle_patch(
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                   # noqa
    @jwt_required()
    @IsAdminOrStaff
    def delete(self, id):
        return tag_controller.handle_delete(id)
