from flask import Response

from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.supermarket.supermarket import (
    Supermarket, SupermarketArea,
    SupermarketAreaIngredientComposite, UserSharedEditSupermarket)
from server.core.models.api_models.supermarket import (
    supermarket_area_ingredinet_model,
    supermarket_area_ingredinet_model_send, supermarket_area_model,
    supermarket_area_model_send,
    supermarket_model, supermarket_model_send, supermarket_user_edit_model)
from server.core.models.db_models.user.user import User
from server.core.models.db_models.recipe.ingredient import Ingredient
from server.errors import http_errors
from server.logger import logger


class SupermarketController(BaseCrudController):
    pass


class SupermarketAreaController(BaseCrudController):
    _model: SupermarketArea

    def handle_get_list(
            self,
            reqargs: dict,
            supermarket_id: int
    ) -> Response:
        try:
            query = self._model.query.filter(
                self._model.supermarket_id == supermarket_id)

            return super().handle_get_list(
                reqargs=reqargs,
                query=query
            )
        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT


class SupermarketAreaIngredientController(BaseCrudController):
    pass


class UserSharedEditSupermarketController(BaseCrudController):
    pass


supermarket_controller = SupermarketController(
    model=Supermarket,
    api_model=supermarket_model,
    api_model_send=supermarket_model_send,
    foreign_key_columns=[
        (User, "owner_user_id")
    ],
    read_only_fields=["owner_user_id"],
    unique_columns_together=["name", "street"],
    use_caching=False
)


supermarket_area_controller = SupermarketAreaController(
    model=SupermarketArea,
    api_model=supermarket_area_model,
    api_model_send=supermarket_area_model_send,
    foreign_key_columns=[
        (Supermarket, "supermarket_id")
    ],
    unique_columns_together=[
        ["supermarket_id", "name"],
        ["supermarket_id", "order_number"]
    ],
    use_caching=True,
    clear_cache_models=[Supermarket]
)


supermarket_area_ingredient_controller = SupermarketAreaIngredientController(
    model=SupermarketAreaIngredientComposite,
    api_model=supermarket_area_ingredinet_model,
    api_model_send=supermarket_area_ingredinet_model_send,
    foreign_key_columns=[
        (SupermarketArea, "sarea_id"),
        (Ingredient, "ingredient_id")
    ],
    read_only_fields=[
        "sarea_id",
        "ingredient_id"
    ],
    unique_columns_together=[
        "sarea_id",
        "ingredient_id"
    ],
    use_caching=True,
    clear_cache_models=[Supermarket, SupermarketArea]
)


user_shared_edit_supermarket_controller = UserSharedEditSupermarketController(
    model=UserSharedEditSupermarket,
    api_model=supermarket_user_edit_model,
    api_model_send=supermarket_user_edit_model,
    foreign_key_columns=[
        (Supermarket, "supermarket_id"),
        (User, "user_id")
    ]
)
