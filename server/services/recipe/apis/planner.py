from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.models.api_models.planner import (
    recipe_planner_item_model,
    recipe_planner_item_model_send, recipe_planner_model,
    recipe_planner_model_send,
    user_shared_recipe_planner_model, user_shared_recipe_planner_model_send)
from server.services.recipe.controller.planner import (
    recipe_planner_controller,
    recipe_planner_item_controller, user_shared_recipe_planner_controller
)


ns = Namespace(
    name="Planner",
    description=__name__,
    path="/api/v1/planner"
)


@ns.route("/")
class RecipePlannerListAPI(Resource):

    @ns.response(code=200, model=[recipe_planner_model], description=sui.desc_list(ns.name))       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        jwt_identity = get_jwt_identity()
        user_id = jwt_identity.get("id")

        return recipe_planner_controller.handle_get_list(
            reqargs=request.args,
            user_id=user_id
        )

    @ns.expect(recipe_planner_model_send)
    @ns.response(code=201, model=recipe_planner_model, description=sui.desc_added(ns.name))        # noqa
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

        return recipe_planner_controller.handle_post(
            data=data
        )


@ns.route("/<int:id>")
class RecipePlannerAPI(Resource):

    @ns.response(code=200, model=recipe_planner_model, description=sui.desc_get(ns.name))   # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return recipe_planner_controller.handle_get(id)  # TODO: here detail model  # noqa

    @ns.expect(recipe_planner_item_model_send)
    @ns.response(code=200, model=recipe_planner_model, description=sui.desc_update(ns.name))       # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def patch(self, id):
        data = request.get_json()
        if "owner_user_id" in data:
            del data["owner_user_id"]

        return recipe_planner_controller.handle_patch(
            id=id,
            data=data
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def delete(self, id):
        return recipe_planner_controller.handle_delete(id)


@ns.route("/item")
class RecipePlannerItemListAPI(Resource):

    @ns.expect(recipe_planner_item_model_send)
    @ns.response(code=201, model=recipe_planner_item_model, description=sui.desc_added("SupermarketAreaIngredient"))     # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("SupermarketAreaIngredient"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def post(self):
        return recipe_planner_item_controller.handle_post(
            data=request.get_json()
        )


@ns.route("/item/<int:id>")
class RecipePlannerItemAPI(Resource):
    @ns.expect(recipe_planner_item_model_send)
    @ns.response(code=200, model=recipe_planner_item_model, description=sui.desc_update("SupermarketAreaIngredient"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("SupermarketAreaIngredient"))            # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                   # noqa
    @jwt_required()
    # @IsRatingOwner
    def patch(self, id):
        # TODO: READ ONLY: [rplanner_id, recipe_id]
        return recipe_planner_item_controller.handle_patch(
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("SupermarketAreaIngredient"))                # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("SupermarketAreaIngredient"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def delete(self, id):
        return recipe_planner_item_controller.handle_delete(id)


@ns.route("/<int:id>/access/user/<int:user_id>")
class UserSharedRecipePlannerAPI(Resource):

    @ns.expect(user_shared_recipe_planner_model_send)
    @ns.response(code=201, model=user_shared_recipe_planner_model, description=sui.desc_added("UserSharedCollection"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                               # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                              # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))               # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("UserSharedCollection"))    # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                               # noqa
    @jwt_required()
    # @IsCollectionOwner
    def post(self, id, user_id):
        data = {
            "rplanner_id": id,
            "user_id": user_id,
            "can_edit": request.get_json().get("can_edit", None)
        }

        return user_shared_recipe_planner_controller.handle_post(
            data=data,
            unique_primarykey=(id, user_id)
        )

    @ns.expect(user_shared_recipe_planner_model_send)
    @ns.response(code=200, model=user_shared_recipe_planner_model, description=sui.desc_update("RecipeIngredient"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("RecipeIngredient"))            # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                   # noqa
    @jwt_required()
    # @IsRatingOwner
    def patch(self, id, user_id):
        return user_shared_recipe_planner_controller.handle_patch(
            id=(id, user_id),
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("CollectionRecipe"))         # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    # @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, user_id):
        return user_shared_recipe_planner_controller.handle_delete(id=(id, user_id))                # noqa
