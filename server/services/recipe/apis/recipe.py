from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.permissions.general import IsAdminOrStaff
from server.core.permissions.recipe import IsRecipeCreatorOrAdminOrStaff
from server.core.models.api_models.recipe import (
    recipe_image_model, recipe_ingredient_model,
    recipe_ingredient_model_send, recipe_model,
    recipe_model_get_list, recipe_model_send,
    recipe_tag_model
)
from server.services.recipe.controller import (
    recipe_controller,
    recipe_ingredient_controller,
    recipe_tag_controller,
    image_controller
)
from server.services.recipe.controller.recipe import recipe_image_controller


ns = Namespace(
    name="Recipe",
    description=__name__,
    path="/api/v1/recipe"
)


@ns.route("/")
class RecipeListAPI(Resource):

    @ns.expect(recipe_model_get_list)
    @ns.response(code=200, model=[recipe_model], description=sui.desc_list(ns.name))            # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        return recipe_controller.handle_get_list(request.args)

    @ns.expect(recipe_model_send)
    @ns.response(code=201, model=recipe_model, description=sui.desc_added(ns.name))             # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        return recipe_controller.handle_post(
            data=request.get_json()
        )


@ns.route("/<int:id>")
class RecipeAPI(Resource):

    @ns.response(code=200, model=recipe_model, description=sui.desc_get(ns.name))               # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return recipe_controller.handle_get(id)

    @ns.expect(recipe_model_send)
    @ns.response(code=200, model=recipe_model, description=sui.desc_update(ns.name))            # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def patch(self, id):
        return recipe_controller.handle_patch(
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
        return recipe_controller.handle_delete(id)


@ns.route("/<int:id>/tag/<int:tag_id>")
class RecipeTagAPI(Resource):

    @ns.response(code=201, model=recipe_tag_model, description=sui.desc_added("RecipeTag"))     # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("RecipeTag"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def post(self, id, tag_id):
        data = {
            "recipe_id": id,
            "tag_id": tag_id
        }

        return recipe_tag_controller.handle_post(
            data=data,
            unique_primarykey=(id, tag_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("RecipeTag"))                # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, tag_id):
        return recipe_tag_controller.handle_delete(
            id=(id, tag_id)
        )


@ns.route("/<int:id>/ingredient/<int:ingredient_id>")
class RecipeIngredientAPI(Resource):

    @ns.expect(recipe_ingredient_model_send)
    @ns.response(code=201, model=recipe_ingredient_model, description=sui.desc_added("RecipeIngredient"))   # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))                   # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("RecipeIngredient"))            # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                   # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def post(self, id, ingredient_id):
        data = {
            "recipe_id": id,
            "ingredient_id": ingredient_id,
            "quantity": request.get_json().get("quantity")
        }

        return recipe_ingredient_controller.handle_post(
            data=data,
            unique_primarykey=(id, ingredient_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("RecipeIngredient"))         # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, ingredient_id):
        return recipe_ingredient_controller.handle_delete(
            id=(id, ingredient_id)
        )


@ns.route("/image")
class RecipeImagePostAPI(Resource):

    @ns.response(code=201, description="Image uploaded successfully")
    @ns.response(code=401, model=error_model, description="Unauthorized")
    @ns.response(code=500, model=error_model, description="Unexpected error")
    @jwt_required()
    def post(self):
        return image_controller.handle_post(request.files)


@ns.route("/image/<int:id>")
class RecipeImageGetAPI(Resource):

    @ns.response(code=200, model=None, description="Image file")
    @ns.response(code=401, model=error_model, description="Unauthorized")                               # noqa
    @ns.response(code=404, model=error_model, description="Image file not found")                       # noqa
    @ns.response(code=500, model=error_model, description="Unexpected error")                           # noqa
    @jwt_required()
    @IsAdminOrStaff
    def get(self, id):
        return image_controller.handle_get(id)


@ns.route("/<int:id>/image/<int:image_id>")
class RecipeImageAPI(Resource):

    @ns.response(code=201, model=recipe_image_model, description=sui.desc_added("RecipeImage"))             # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))                   # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("RecipeImage"))                 # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                   # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def post(self, id, image_id):
        data = {
            "recipe_id": id,
            "image_id": image_id
        }

        return recipe_image_controller.handle_post(
            data=data,
            unique_primarykey=(id, image_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("RecipeImage"))              # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, image_id):
        return recipe_image_controller.handle_delete(
            id=(id, image_id)
        )
