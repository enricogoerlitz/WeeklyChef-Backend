from flask import Response

from server.core.models.db_models.recipe.collection import (
    Collection, CollectionRecipeComposite,
    UserSharedCollection)
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.api_models.recipe import (
    collection_model, collection_model_send,
    collection_recipe_model, user_shared_collection_model,
    user_shared_collection_model_send)
from server.core.models.db_models.user.user import User
from server.core.models.db_models.recipe.recipe import Recipe
from server.errors import http_errors
from server.logger import logger


class CollectionController(BaseCrudController):
    _model: Collection

    def handle_get_list(self, reqargs: dict, user_id: int) -> Response:
        try:
            query_collection_owner = self._model.query.filter(
                self._model.owner_user_id == user_id)

            query_collection_shared = self._model.query \
                .join(UserSharedCollection) \
                .filter(UserSharedCollection.user_id == user_id)

            query = query_collection_owner.union(query_collection_shared)

            return super().handle_get_list(
                reqargs=reqargs,
                query=query,
                redis_addition_key=f"uid:{user_id}"
            )
        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT


class CollectionRecipeController(BaseCrudController):
    pass


class UserSharedCollectionController(BaseCrudController):
    pass


collection_controller = CollectionController(
    model=Collection,
    api_model=collection_model,
    api_model_send=collection_model_send,
    search_fields=["name"],
    unique_columns_together=[
        "name",
        "owner_user_id"
    ],
    foreign_key_columns=[
        (User, "owner_user_id")
    ],
    read_only_fields=["owner_user_id"],
    use_caching=True
)


collection_recipe_controller = CollectionRecipeController(
    model=CollectionRecipeComposite,
    api_model=collection_recipe_model,
    api_model_send=collection_recipe_model,
    foreign_key_columns=[
        (Collection, "collection_id"),
        (Recipe, "recipe_id")
    ],
    unique_columns_together=[
        "collection_id",
        "recipe_id"
    ],
    use_caching=True,
    clear_cache_models=[Collection]
)


user_shared_collection_controller = UserSharedCollectionController(
    model=UserSharedCollection,
    api_model=user_shared_collection_model,
    api_model_send=user_shared_collection_model_send,
    foreign_key_columns=[
        (Collection, "collection_id"),
        (User, "user_id")
    ],
    unique_columns_together=[
        "collection_id",
        "user_id"
    ],
    use_caching=True,
    clear_cache_models=[Collection]
)
