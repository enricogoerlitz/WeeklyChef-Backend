from flask import Response

from server.core.models.db_models.cart import (
    Cart, CartItem, UserSharedEditCart
)
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.api_models.cart import (
    cart_item_model, cart_item_model_send, cart_model,
    cart_model_detail, cart_model_send, user_shared_cart_model)
from server.core.models.db_models.recipe import Recipe
from server.core.models.db_models.ingredient import Ingredient
from server.errors import http_errors, errors
from server.logger import logger
from server.db import db


class CartController(BaseCrudController):
    _model: Cart

    def handle_get_list(
            self,
            reqargs: dict,
            user_id: int
    ) -> Response:
        try:
            query_cart_owner = self._model.query.filter(
                self._model.owner_user_id == user_id)

            query_cart_shared = self._model.query \
                .join(UserSharedEditCart) \
                .filter(UserSharedEditCart.user_id == user_id)

            query = query_cart_owner.union(query_cart_shared)

            return super().handle_get_list(
                reqargs=reqargs,
                query=query,
                redis_addition_key=f"uid:{user_id}"
            )
        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    def handle_clear_cart(self, cart_id: int):
        try:
            # Validate correct Cart
            _ = self._find_object_by_id(cart_id)

            db.session.query(CartItem) \
                .filter(CartItem.cart_id == cart_id) \
                .delete()
            db.session.commit()

            self._clear_cache()

            return "", 204

        except errors.DbModelNotFoundException as e:
            return http_errors.not_found(e)

        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT


class CartItemController(BaseCrudController):
    pass


class UserSharedCartController(BaseCrudController):
    pass


cart_controller = CartController(
    model=Cart,
    api_model=cart_model,
    api_model_detail=cart_model_detail,
    api_model_send=cart_model_send,
    read_only_fields=["owner_user_id"],
    unique_columns_together=["name", "owner_user_id"]
)

cart_item_controller = CartItemController(
    model=CartItem,
    api_model=cart_item_model,
    api_model_send=cart_item_model_send,
    foreign_key_columns=[
        (Cart, "cart_id"),
        (Recipe, "recipe_id"),
        (Ingredient, "ingredient_id"),
    ],
    read_only_fields=[
        "cart_id",
        "recipe_id",
        "ingredient_id"
    ],
    clear_cache_models=[Cart]
)

user_shared_cart_controller = UserSharedCartController(
    model=UserSharedEditCart,
    api_model=user_shared_cart_model,
    api_model_send=user_shared_cart_model,
    foreign_key_columns=[
        (Cart, "cart_id")
    ],
    read_only_fields=["cart_id", "user_id"],
    unique_columns_together=["cart_id", "user_id"],
    clear_cache_models=[Cart]
)
