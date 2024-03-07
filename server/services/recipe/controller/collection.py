from flask import Response
from flask_sqlalchemy.model import Model

from server.api import api
from server.core.models.db_models.recipe.collection import (
    Collection, CollectionRecipeComposite,
    UserSharedCollection)
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.api_models.recipe import (
    collection_model, collection_model_send,
    collection_recipe_model, user_shared_collection_model,
    user_shared_collection_model_send)


class CollectionController(BaseCrudController):
    _model: Collection

    def __init__(
            self,
            model: Model,
            api_model: api.model,  # type: ignore
            api_model_send: api.model = None,  # type: ignore
            unique_columns: list[str] = None,
            search_fields: list[str] = None,
            pagination_page_size: int = 20,
            use_caching: bool = True,
            clear_cache_models: list[Model] = None
    ) -> None:
        super().__init__(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            unique_columns=unique_columns,
            search_fields=search_fields,
            pagination_page_size=pagination_page_size,
            use_caching=use_caching,
            clear_cache_models=clear_cache_models
        )

    def handle_get_list(self, reqargs: dict, user_id: int) -> Response:
        # TODO: Add Try Catch
        # TODO: man sieht auch die, die mit einem geteilt sind!
        # return super().handle_get_list(reqargs=reqargs)
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


collection_controller = CollectionController(
    model=Collection,
    api_model=collection_model,
    api_model_send=collection_model_send,
    unique_columns=["name"],
    search_fields=["name"],
    pagination_page_size=20,
    use_caching=True
)

collection_recipe_controller = BaseCrudController(
    model=CollectionRecipeComposite,
    api_model=collection_recipe_model,
    api_model_send=collection_recipe_model,
    unique_columns=None,
    search_fields=None,
    pagination_page_size=20,
    use_caching=True,
    clear_cache_models=[Collection]
)


user_shared_collection_controller = BaseCrudController(
    model=UserSharedCollection,
    api_model=user_shared_collection_model,
    api_model_send=user_shared_collection_model_send,
    use_caching=True,
    clear_cache_models=[Collection]
)
