from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.utils import swagger as sui
from server.core.models.api_models.supermarket import (
    supermarket_area_ingredinet_model,
    supermarket_area_ingredinet_model_send, supermarket_area_model,
    supermarket_area_model_send,
    supermarket_model, supermarket_model_detail, supermarket_model_send)
from server.core.models.api_models.utils import error_model
from server.services.recipe.controller.supermarket import (
    supermarket_area_controller,
    supermarket_area_ingredient_controller, supermarket_controller,
    user_shared_edit_supermarket_controller)


ns = Namespace(
    name="Supermarket",
    description=__name__,
    path="/api/v1/supermarket"
)


@ns.route("/")
class SupermarketListAPI(Resource):

    @ns.response(code=200, model=[supermarket_model], description=sui.desc_list(ns.name))       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        return supermarket_controller.handle_get_list(request.args)

    @ns.expect(supermarket_model_send)
    @ns.response(code=201, model=supermarket_model, description=sui.desc_added(ns.name))        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def post(self):
        jwt_identity = get_jwt_identity()
        user_id = jwt_identity.get("id")

        data = request.get_json()
        data["owner_user_id"] = user_id

        return supermarket_controller.handle_post(
            data=data
        )


@ns.route("/<int:id>")
class SupermarketAPI(Resource):

    @ns.response(code=200, model=supermarket_model_detail, description=sui.desc_get(ns.name))   # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return supermarket_controller.handle_get(
            id=id,
            api_response_model=supermarket_model_detail
        )

    @ns.expect(supermarket_model_send)
    @ns.response(code=200, model=supermarket_model, description=sui.desc_update(ns.name))       # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def patch(self, id):
        data = request.get_json()
        if "owner_user_id" in data:
            del data["owner_user_id"]

        return supermarket_controller.handle_patch(
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def delete(self, id):
        return supermarket_controller.handle_delete(id)


@ns.route("/<int:id>/area")
class SupermarketAreaListAPI(Resource):

    @ns.response(code=200, model=[supermarket_area_model], description="Areas of given Supermarket")  # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return supermarket_area_controller.handle_get_list(
            reqargs=request.args,
            supermarket_id=id,
        )

    @ns.expect(supermarket_area_model_send)
    @ns.response(code=201, model=supermarket_area_model, description=sui.desc_added("SupermarketArea"))        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("SupermarketArea"))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def post(self, id):
        data = request.get_json()
        data["supermarket_id"] = id

        return supermarket_area_controller.handle_post(
            data=data
        )


@ns.route("/area/<int:id>")
class SupermarketAreaAPI(Resource):

    @ns.expect(supermarket_area_model_send)
    @ns.response(code=200, model=supermarket_area_model, description=sui.desc_update("SupermarketArea"))       # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("SupermarketArea"))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def patch(self, id):
        return supermarket_area_controller.handle_patch(
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def delete(self, id):
        return supermarket_area_controller.handle_delete(id)


@ns.route("/area/<int:sarea_id>/ingredient/<int:ingredient_id>")
class SupermarketAreaIngredientAPI(Resource):

    @ns.expect(supermarket_area_ingredinet_model_send)
    @ns.response(code=201, model=supermarket_area_ingredinet_model, description=sui.desc_added("SupermarketAreaIngredient"))     # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("SupermarketAreaIngredient"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def post(self, sarea_id, ingredient_id):
        data = {
            "sarea_id": sarea_id,
            "ingredient_id": ingredient_id,
            "ingredient_price": request.get_json().get("ingredient_price")
        }

        return supermarket_area_ingredient_controller.handle_post(
            data=data,
            unique_primarykey=(sarea_id, ingredient_id)
        )

    @ns.expect(supermarket_area_ingredinet_model_send)
    @ns.response(code=200, model=supermarket_area_ingredinet_model, description=sui.desc_update("SupermarketAreaIngredient"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("SupermarketAreaIngredient"))            # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                   # noqa
    @jwt_required()
    # @IsRatingOwner
    def patch(self, sarea_id, ingredient_id):
        return supermarket_area_ingredient_controller.handle_patch(
            id=(sarea_id, ingredient_id),
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("SupermarketAreaIngredient"))                # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("SupermarketAreaIngredient"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def delete(self, sarea_id, ingredient_id):
        return supermarket_area_ingredient_controller.handle_delete(
            id=(sarea_id, ingredient_id)
        )


@ns.route("/<int:id>/access/edit/user/<int:user_id>")
class UserSharedEditSupermarketAPI(Resource):

    @ns.response(code=201, model=supermarket_area_ingredinet_model, description=sui.desc_added("UserSharedEditSupermarket"))     # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("UserSharedEditSupermarket"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def post(self, id, user_id):
        data = {
            "supermarket_id": id,
            "user_id": user_id
        }

        return user_shared_edit_supermarket_controller.handle_post(
            data=data,
            unique_primarykey=(id, user_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("UserSharedEditSupermarket"))                # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("UserSharedEditSupermarket"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def delete(self, id, user_id):
        return user_shared_edit_supermarket_controller.handle_delete(
            id=(id, user_id)
        )
