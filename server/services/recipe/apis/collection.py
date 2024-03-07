from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity

from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.permissions.general import IsAdminOrStaff
from server.core.models.api_models.recipe import (
    collection_model, collection_model_send,
    user_shared_collection_model, user_shared_collection_model_send
)
from server.services.recipe.controller.collection import (
    collection_controller,
    collection_recipe_controller,
    user_shared_collection_controller)


ns = Namespace(
    name="Collection",
    description=__name__,
    path="/api/v1/collection"
)


@ns.route("/")
class CollectionListAPI(Resource):

    @ns.response(code=200, model=[collection_model], description=sui.desc_list(ns.name))        # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        jwt_identity: dict = get_jwt_identity()
        user_id = jwt_identity.get("id")

        return collection_controller.handle_get_list(
            reqargs=request.args,
            user_id=user_id
        )

    @ns.expect(collection_model_send)
    @ns.response(code=201, model=collection_model, description=sui.desc_added(ns.name))         # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    # @IsCollectionOwnerOrCanEdit
    def post(self):
        jwt_identity: dict = get_jwt_identity()
        user_id = jwt_identity.get("id")

        data = request.get_json()
        data["owner_user_id"] = user_id

        return collection_controller.handle_post(
            data=data
        )


@ns.route("/<int:id>")
class CollectionAPI(Resource):

    @ns.response(code=200, model=collection_model, description=sui.desc_get(ns.name))           # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return collection_controller.handle_get(id)

    @ns.expect(collection_model_send)
    @ns.response(code=200, model=collection_model, description=sui.desc_update(ns.name))        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    # @IsCollectionOwnerOrCanEdit
    def patch(self, id):
        data = request.get_json()
        if "owner_user_id" in data:
            del data["owner_user_id"]

        return collection_controller.handle_patch(
            id=id,
            data=data
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def delete(self, id):
        return collection_controller.handle_delete(id)


@ns.route("/<int:id>/access/user/<int:user_id>")
class UserSharedCollectionAPI(Resource):

    @ns.expect(user_shared_collection_model_send)
    @ns.response(code=201, model=user_shared_collection_model, description=sui.desc_added("UserSharedCollection"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                               # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                              # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))               # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("UserSharedCollection"))    # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                               # noqa
    @jwt_required()
    # @IsCollectionOwner
    def post(self, id, user_id):
        data = {
            "collection_id": id,
            "user_id": user_id,
            "can_edit": request.get_json().get("can_edit", None)
        }

        return user_shared_collection_controller.handle_post(
            data=data,
            unique_primarykey=(id, user_id)
        )

    @ns.expect(user_shared_collection_model_send)
    @ns.response(code=200, model=user_shared_collection_model, description=sui.desc_update("RecipeIngredient"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("RecipeIngredient"))            # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                   # noqa
    @jwt_required()
    # @IsRatingOwner
    def patch(self, id, user_id):
        return user_shared_collection_controller.handle_patch(
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
        return user_shared_collection_controller.handle_delete(id=(id, user_id))                # noqa


@ns.route("/<int:id>/recipe/<int:recipe_id>")
class CollectionRecipeAPI(Resource):

    @ns.response(code=201, model=collection_model, description=sui.desc_added("CollectionRecipe"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))           # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("CollectionRecipe"))    # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    # @IsCollectionOwner
    def post(self, id, recipe_id):
        data = {
            "collection_id": id,
            "recipe_id": recipe_id
        }

        return collection_recipe_controller.handle_post(
            data=data,
            unique_primarykey=(id, recipe_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("CollectionRecipe"))         # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    # @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, recipe_id):
        return collection_recipe_controller.handle_delete(id=(id, recipe_id))
