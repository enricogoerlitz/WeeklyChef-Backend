import os
import uuid

from werkzeug.datastructures import FileStorage, ImmutableMultiDict

from sqlalchemy import or_
from flask import Response, send_file
from flask_sqlalchemy.model import Model
from flask_sqlalchemy.query import Query

from server.db import db
from server.api import api
from server.errors import errors, http_errors
from server.core.controller.crud_controller import (
    BaseCrudController, IController
)
from server.core.models.db_models.recipe.recipe import (
    Recipe, RecipeImage, RecipeIngredient,
    RecipeTagComposite, ReicpeImageComposite
)
from server.core.models.api_models.recipe import (
    recipe_image_model, recipe_ingredient_model,
    recipe_ingredient_model_send, recipe_model,
    recipe_model_send, recipe_tag_model
)
from server.core.models.db_models.recipe.tag import Tag
from server.core.models.db_models.recipe.ingredient import Ingredient
from server.core.models.db_models.recipe.category import Category
from server.logger import logger


class RecipeController(BaseCrudController):

    def __init__(
            self,
            model: Model,
            api_model: api.model,  # type: ignore
            api_model_send: api.model = None,  # type: ignore
            unique_columns: list[str] = None,
            search_fields: list[str] = None,
            pagination_page_size: int = 20,
            use_redis: bool = True
    ) -> None:
        super().__init__(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            unique_columns=unique_columns,
            search_fields=search_fields,
            pagination_page_size=pagination_page_size,
            use_redis=use_redis
        )

    def handle_get_list(self, reqargs: dict) -> Response:
        # OVERRIDE
        # HIER zusätzlich suche nach TAG und INGREDIENT einbauen!
        # model_query = ...filter() -> an handle_get_list query übergeben!
        search = reqargs.get("search")
        difficulty_search = reqargs.get("difficulty")
        query: Query = self._model.query

        if search is not None:
            search_str = f"%{search}%"

            query_recipe = query.filter(
                or_(
                    Recipe.name.like(search_str),
                    Recipe.search_description.like(search_str),
                    Recipe.preperation_description.like(search_str)
                )
            )

            query_tag_search = query \
                .join(RecipeTagComposite) \
                .join(Tag) \
                .filter(Tag.name.like(search_str))

            query_ingredient_search = query \
                .join(RecipeIngredient) \
                .join(Ingredient) \
                .filter(Ingredient.name.like(search_str))

            query_category_search = query.join(Category).filter(
                Category.name.like(search_str)
            )

            query = query_recipe.union(query_tag_search) \
                                .union(query_ingredient_search) \
                                .union(query_category_search)

        if difficulty_search is not None:
            query = query.filter(Recipe.difficulty == difficulty_search)

        return super().handle_get_list(reqargs, query=query)


class ImageController(IController):

    def __init__(self) -> None:
        self._model = RecipeImage
        self._upload_folder = "/images"
        self._image_req_key = "recipe_image"
        self._allowed_extension = {"png", "jpg", "jpeg"}

    def handle_get(self, id: int) -> Response:
        try:
            recipe_image: RecipeImage = RecipeImage.query.get(id)
            if recipe_image is None:
                raise errors.ImageNotFoundException(id)

            return send_file(recipe_image.path)
        except errors.ImageNotFoundException as e:
            return http_errors.not_found(e)

        except IOError:
            err_msg = f"The image id '{id}' is existing, but the file was not found!"  # noqa
            logger.error(err_msg)
            return http_errors.server_error(err_msg)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_post(
            self,
            files: ImmutableMultiDict[str, FileStorage]
    ) -> Response:
        try:
            file = files.get(self._image_req_key)
            file_extension = self._get_file_extension(file)

            self._validate_file(file, file_extension)

            filename = str(uuid.uuid4()) + "." + file_extension
            filepath = os.path.join(self._upload_folder, filename)

            file.save(filepath)

            recipe_image = RecipeImage(path=filepath)
            db.session.add(recipe_image)
            db.session.commit()

            return {"id": recipe_image.id}, 200

        except (errors.ImageNotGivenException,
                errors.ImageNotAllowedFileExtensionException) as e:
            return http_errors.bad_request(e)

        except Exception as e:
            logger.error(f"{str(e)}")
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_get_list(self): raise NotImplementedError()

    def handle_patch(self): raise NotImplementedError()

    def handle_delete(self): raise NotImplementedError()

    def _validate_file(
            self, file: FileStorage | None,
            file_extension: str
    ) -> None:
        if file is None or file.filename == "":
            raise errors.ImageNotGivenException(self._image_req_key)

        if file_extension not in self._allowed_extension:
            raise errors.ImageNotAllowedFileExtensionException(
                file_extension=file_extension,
                allowed_file_extensions=self._allowed_extension
            )

    def _get_file_extension(self, file: FileStorage) -> str:
        if file is None or "." not in file.filename:
            return ""

        return file.filename.rsplit(".", 1)[1].lower()


recipe_controller = RecipeController(
    model=Recipe,
    api_model=recipe_model,
    api_model_send=recipe_model_send,
    unique_columns=["name"],
    search_fields=[
        "name",
        "search_description",
        "preperation_description"
    ],
    pagination_page_size=20,
    use_redis=True  # CHANGE HERE
)


recipe_ingredient_controller = BaseCrudController(
    model=RecipeIngredient,
    api_model=recipe_ingredient_model,
    api_model_send=recipe_ingredient_model_send,
    unique_columns=None,
    search_fields=None,
    pagination_page_size=20,
    use_redis=True
)


recipe_tag_controller = BaseCrudController(
    model=RecipeTagComposite,
    api_model=recipe_tag_model,
    api_model_send=recipe_tag_model,
    unique_columns=None,
    search_fields=None,
    pagination_page_size=20,
    use_redis=True
)


image_controller = ImageController()


recipe_image_controller = BaseCrudController(
    model=ReicpeImageComposite,
    api_model=recipe_image_model,
    api_model_send=recipe_image_model,
    unique_columns=None,
    search_fields=None,
    pagination_page_size=20,
    use_redis=True
)
