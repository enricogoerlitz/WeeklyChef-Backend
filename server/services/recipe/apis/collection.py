"""
RecipeCollection Routes
"""

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from utils import swagger as sui
from core.controller import crud_controller
from core.models.api_models.utils import error_model
from core.permissions.general import IsAdminOrStaff
from core.models.api_models.recipe import (
    collection_model, collection_model_send,
    collection_recipe_model,
    collection_user_model, collection_user_model_send
)
from core.models.db_models import (
    Collection,
    CollectionRecipeComposite
)


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
        return crud_controller.handle_get_list(
            model=Collection,
            api_model=collection_model
        )

    @ns.expect(collection_model_send)
    @ns.response(code=201, model=collection_model, description=sui.desc_added(ns.name))         # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        return crud_controller.handle_post(
            model=Collection,
            api_model=collection_model,
            api_model_send=collection_model_send,
            data=request.get_json()
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
        return crud_controller.handle_get(Collection, collection_model, id)

    @ns.expect(collection_model_send)
    @ns.response(code=200, model=collection_model, description=sui.desc_update(ns.name))        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def patch(self, id):
        return crud_controller.handle_patch(
            model=Collection,
            api_model=collection_model,
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
        return crud_controller.handle_delete(Collection, id)


@ns.route("/<int:id>/users/<int:user_id>")
class UserSharedCollectionAPI(Resource):

    @ns.expect(collection_user_model_send)
    @ns.response(code=201, model=collection_user_model, description=sui.desc_added("UserSharedCollection"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                               # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                              # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))               # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("UserSharedCollection"))    # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                               # noqa
    @jwt_required()
    # @IsRecipeCreatorOrAdminOrStaff
    def post(self, id, user_id):
        data = {
            "collection_id": id,
            "user_id": user_id,
            "can_edit": request.get_json().get("can_edit", None)
        }

        return crud_controller.handle_post(
            model=CollectionRecipeComposite,
            api_model=collection_user_model,
            api_model_send=collection_user_model_send,
            data=data,
            unique_primarykey=(id, user_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("CollectionRecipe"))         # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    # @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, user_id):
        return crud_controller.handle_delete(
            CollectionRecipeComposite,
            (id, user_id)
        )


@ns.route("/<int:id>/recipe/<int:recipe_id>")
class CollectionRecipeAPI(Resource):

    @ns.response(code=201, model=collection_model, description=sui.desc_added("CollectionRecipe"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))           # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("CollectionRecipe"))    # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    # @IsRecipeCreatorOrAdminOrStaff
    def post(self, id, recipe_id):
        data = {
            "collection_id": id,
            "recipe_id": recipe_id
        }

        return crud_controller.handle_post(
            model=CollectionRecipeComposite,
            api_model=collection_recipe_model,
            api_model_send=collection_recipe_model,
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
        return crud_controller.handle_delete(
            CollectionRecipeComposite,
            (id, recipe_id)
        )
