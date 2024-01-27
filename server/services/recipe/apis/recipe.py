"""
Recipe Routes

- recipe
- recipe<-tag           /recipe/<int:id>/tag/<int:tag_id>
- recipe<-ingredient
- recipe<-image
"""

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from utils import swagger as sui
from core.controller import crud_controller
from core.models.api_models.utils import error_model
from core.permissions.general import IsAdminOrStaff
from core.permissions.recipe import IsRecipeCreatorOrAdminOrStaff
from core.models.api_models.recipe import (
    recipe_model, recipe_model_send,
    recipe_tag_model,
    recipe_ingredient_model, recipe_ingredient_model_send
)
from core.models.db_models import (
    Recipe,
    RecipeTagComposite,
    RecipeIngredient
)


ns = Namespace(
    name="Recipe",
    description=__name__,
    path="/api/v1/recipe"
)


@ns.route("/")
class RecipeListAPI(Resource):

    @ns.response(code=200, model=[recipe_model], description=sui.desc_list(ns.name))            # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        return crud_controller.handle_get_list(
            model=Recipe,
            api_model=recipe_model
        )

    @ns.expect(recipe_model_send)
    @ns.response(code=201, model=recipe_model, description=sui.desc_added(ns.name))             # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        return crud_controller.handle_post(
            model=Recipe,
            api_model=recipe_model,
            api_model_send=recipe_model_send,
            data=request.get_json(),
            unique_columns=["name"]
        )


@ns.route("/<int:id>")
class RecipeAPI(Resource):

    @ns.response(code=200, model=recipe_model, description=sui.desc_get(ns.name))               # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self, id):
        return crud_controller.handle_get(Recipe, recipe_model, id)

    @ns.expect(recipe_model_send)
    @ns.response(code=200, model=recipe_model, description=sui.desc_update(ns.name))            # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def put(self, id):
        return crud_controller.handle_update(
            model=Recipe,
            api_model=recipe_model,
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsAdminOrStaff
    def delete(self, id):
        return crud_controller.handle_delete(Recipe, id)


@ns.route("/<int:id>/tag/<int:tag_id>")
class RecipeTagAPI(Resource):

    @ns.response(code=201, model=recipe_tag_model, description=sui.desc_added("RecipeTag"))     # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("RecipeTag"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def post(self, id, tag_id):
        data = {
            "recipe_id": id,
            "tag_id": tag_id
        }

        return crud_controller.handle_post(
            model=RecipeTagComposite,
            api_model=recipe_tag_model,
            api_model_send=recipe_tag_model,
            data=data,
            unique_primarykey=(id, tag_id)
        )


    @ns.response(code=204, model=None, description=sui.desc_delete("RecipeTag"))                # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, tag_id):
        return crud_controller.handle_delete(RecipeTagComposite, (id, tag_id))


@ns.route("/<int:id>/ingredient/<int:ingredient_id>")
class RecipeIngredientAPI(Resource):

    @ns.expect(recipe_ingredient_model_send)
    @ns.response(code=201, model=recipe_ingredient_model, description=sui.desc_added("RecipeIngredient"))   # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                  # noqa
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

        return crud_controller.handle_post(
            model=RecipeIngredient,
            api_model=recipe_ingredient_model,
            api_model_send=recipe_ingredient_model_send,
            data=data,
            unique_primarykey=(id, ingredient_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("RecipeIngredient"))         # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsRecipeCreatorOrAdminOrStaff
    def delete(self, id, ingredient_id):
        return crud_controller.handle_delete(
            RecipeIngredient, (id, ingredient_id))
