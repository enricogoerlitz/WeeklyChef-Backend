"""
"""

from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required


from core.controller import crud_controller
from core.models.api_models.utils import error_model
from core.permissions.general import IsAdminOrStaff, IsAdmin
from core.models.api_models.recipe import (
    category_model, category_model_send,
    tag_model, tag_model_send,
    unit_model, unit_model_send,
    ingredient_model, ingredient_model_send,
    recipe_model, recipe_model_send
)
from core.models.db_models import (
    Category,
    Tag,
    Unit,
    Ingredient,
    Recipe
)


ns = Namespace(
    name="Recipe",
    description=__name__,
    path="/api/v1/"
)


@ns.route("/category")
class CategoryListAPI(Resource):

    @ns.response(code=200, model=[category_model], description="Returns list of Categories")    # noqa
    @ns.response(code=401, model=error_model, description="Returns User unauthorized Error")    # noqa
    @ns.response(code=500, model=error_model, description="Returns unexpected Error")           # noqa
    @jwt_required()
    def get(self):
        return crud_controller.handle_get_list(
            model=Category,
            api_model=category_model
        )

    @ns.expect(category_model_send)
    @ns.response(code=200, model=category_model, description="Adds a new Category")             # noqa
    @ns.response(code=400, model=error_model, description="Returns invalied User input Error")  # noqa
    @ns.response(code=401, model=error_model, description="Returns User unauthorized Error")    # noqa
    @ns.response(code=409, model=error_model, description="Category is already existing")       # noqa
    @ns.response(code=500, model=error_model, description="Returns unexpected Error")           # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        return crud_controller.handle_post(
            model=Category,
            api_model=category_model,
            unique_columns=["name"]
        )


@ns.route("/category/<int:id>")
class CategoryAPI(Resource):

    @ns.response(code=200, model=category_model, description="Returns Category by ID")          # noqa
    @ns.response(code=400, model=error_model, description="Returns Error")                      # noqa
    @ns.response(code=401, model=error_model, description="Returns User unauthorized Error")    # noqa
    @ns.response(code=500, model=error_model, description="Returns unexpected Error")           # noqa
    @jwt_required()
    def get(self, id):
        return crud_controller.handle_get(Category, category_model, id)

    @ns.expect(category_model_send)
    @ns.response(code=200, model=category_model, description="Add category")                    # noqa
    @ns.response(code=400, model=error_model, description="Returns Error")                      # noqa
    @ns.response(code=401, model=error_model, description="Returns User unauthorized Error")    # noqa
    @ns.response(code=500, model=error_model, description="Unexpected error")                   # noqa
    @jwt_required()
    @IsAdminOrStaff
    def put(self, id):
        return crud_controller.handle_update(
            model=Category,
            api_model=category_model,
            id=id
        )

    @ns.expect(category_model_send)
    @ns.response(code=200, model=category_model, description="Add category")                    # noqa
    @ns.response(code=400, model=error_model, description="Returns Error")                      # noqa
    @ns.response(code=401, model=error_model, description="Returns User unauthorized Error")    # noqa
    @ns.response(code=500, model=error_model, description="Unexpected error")                   # noqa
    @jwt_required()
    @IsAdminOrStaff
    def patch(self, id):
        return crud_controller.handle_update(
            model=Category,
            api_model=category_model,
            id=id
        )

    @ns.response(code=200, model=[category_model], description="Add category")                  # noqa
    @ns.response(code=400, model=error_model, description="Returns Error")                      # noqa
    @ns.response(code=401, model=error_model, description="Returns User unauthorized Error")    # noqa
    @ns.response(code=500, model=error_model, description="Unexpected error")                   # noqa
    @jwt_required()
    @IsAdmin
    def delete(self, id):
        return crud_controller.handle_delete(Category, id)


@ns.route("/recipe")
class RecipeListAPI(Resource):

    @ns.response(code=200, model=[recipe_model], description="List of user models")             # noqa
    @ns.response(code=500, model=error_model, description="List of user models")                # noqa
    def get(self):
        return crud_controller.handle_get_list(Recipe, recipe_model)
