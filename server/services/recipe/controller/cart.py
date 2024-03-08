from flask import Response
from flask_sqlalchemy.model import Model

from server.api import api
from server.core.models.db_models.cart.cart import (
    Cart, CartItem, UserSharedCart
)
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.api_models.cart import (
    cart_item_model, cart_item_model_send, cart_model,
    cart_model_send, user_shared_cart_model)


class CartController(BaseCrudController):
    _model: Cart

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
        query_cart_owner = self._model.query.filter(
            self._model.owner_user_id == user_id)

        query_cart_shared = self._model.query \
            .join(UserSharedCart) \
            .filter(UserSharedCart.user_id == user_id)

        query = query_cart_owner.union(query_cart_shared)

        return super().handle_get_list(
            reqargs=reqargs,
            query=query,
            redis_addition_key=f"uid:{user_id}"
        )


cart_controller = CartController(
    model=Cart,
    api_model=cart_model,
    api_model_send=cart_model_send,
    use_caching=True
)


cart_item_controller = BaseCrudController(
    model=CartItem,
    api_model=cart_item_model,
    api_model_send=cart_item_model_send,
    use_caching=True,
    clear_cache_models=[Cart]
)


user_shared_cart_controller = BaseCrudController(
    model=UserSharedCart,
    api_model=user_shared_cart_model,
    api_model_send=user_shared_cart_model,
    use_caching=True,
    clear_cache_models=[Cart]
)
