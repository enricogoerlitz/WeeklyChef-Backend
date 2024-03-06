import os
import uuid

from flask import request, send_from_directory
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.permissions.general import IsAdminOrStaff
from server.core.permissions.recipe import IsRecipeCreatorOrAdminOrStaff
from server.core.models.api_models.recipe import (
    recipe_model, recipe_model_send,
    recipe_tag_model,
    recipe_ingredient_model, recipe_ingredient_model_send,
    recipe_model_get_list
)
from server.services.recipe.controller import (
    recipe_controller,
    recipe_ingredient_controller,
    recipe_tag_controller
)


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


# TODO: fix this!
UPLOAD_FOLDER = "/images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@ns.route("/image")
class RecipeImageAPI(Resource):

    @ns.response(code=200, description="List of all image filenames")
    @ns.response(code=401, description="Unauthorized")
    @ns.response(code=500, description="Unexpected error")
    def get(self):
        filenames = os.listdir(UPLOAD_FOLDER)[1]
        return send_from_directory(UPLOAD_FOLDER, filenames)
        return filenames, 200

    @ns.response(code=201, description="Image uploaded successfully")
    @ns.response(code=401, description="Unauthorized")
    @ns.response(code=500, description="Unexpected error")
    @jwt_required()
    def post(self):
        if "file" not in request.files:
            return {"message": "No file part"}, 400

        file = request.files["file"]

        if file.filename == "":
            return {"message": "No selected file"}, 400

        if file and allowed_file(file.filename):
            _, file_extension = os.path.splitext(file.filename)
            filename = str(uuid.uuid4()) + file_extension
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return {"message": "Image uploaded successfully"}, 201
        else:
            return {"message": "Invalid file format"}, 400


@ns.route("/image/<filename>")
class RecipeImageFileAPI(Resource):

    @ns.response(code=200, description="Image file")
    @ns.response(code=401, description="Unauthorized")
    @ns.response(code=404, description="Image file not found")
    @ns.response(code=500, description="Unexpected error")
    @jwt_required()
    @IsAdminOrStaff
    def get(self, filename):
        return send_from_directory(UPLOAD_FOLDER, filename)
