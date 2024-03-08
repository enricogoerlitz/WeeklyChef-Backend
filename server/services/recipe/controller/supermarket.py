import typing

from flask import Response
from flask_sqlalchemy.model import Model
from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.supermarket.supermarket import (
    Supermarket, SupermarketArea,
    SupermarketAreaIngredientComposite, UserSharedEditSupermarket)
from server.core.models.api_models.supermarket import (
    supermarket_area_ingredinet_model,
    supermarket_area_ingredinet_model_send, supermarket_area_model,
    supermarket_area_model_send,
    supermarket_model, supermarket_model_send, supermarket_user_edit_model)
from server.api import api


class SupermarketAreaController(BaseCrudController):
    _model: SupermarketArea

    def __init__(
            self,
            model: Model,
            api_model: api.model,  # type: ignore
            api_model_send: api.model = None,  # type: ignore
            unique_columns: list[str] = None,
            search_fields: list[str] = None,
            pagination_page_size: int = 20,
            foreign_key_columns: list[tuple[Model, typing.Any]] = None,
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
            foreign_key_columns=foreign_key_columns,
            use_caching=use_caching,
            clear_cache_models=clear_cache_models
        )

    def handle_get_list(
            self,
            reqargs: dict,
            supermarket_id: int
    ) -> Response:
        # TODO: Add try catch
        query = self._model.query.filter(
            self._model.supermarket_id == supermarket_id)

        return super().handle_get_list(
            reqargs=reqargs,
            query=query
        )

    def handle_post(
            self,
            data: dict
    ) -> Response:
        # TODO: Add try catch
        # TODO: Validate sm-id + ordernumber unique
        # TODO: Validate sm-id + name unique
        # TODO: unique together in CURD Controller!
        # db.query get object!
        return super().handle_post(data)

    def handle_patch(
            self,
            id: typing.Any,
            data: dict
    ) -> Response:
        # TODO: Add try catch
        # TODO: Validate sm-id + ordernumber unique
        # TODO: Validate sm-id + name unique
        # TODO: unique together in CURD Controller!
        # db.query get object!
        return super().handle_patch(id, data)


supermarket_controller = BaseCrudController(
    model=Supermarket,
    api_model=supermarket_model,
    api_model_send=supermarket_model_send,
    use_caching=False
)


supermarket_area_controller = SupermarketAreaController(
    model=SupermarketArea,
    api_model=supermarket_area_model,
    api_model_send=supermarket_area_model_send,
    foreign_key_columns=[
        (Supermarket, "supermarket_id")
    ],
    use_caching=True,
    clear_cache_models=[Supermarket]
)


supermarket_area_ingredient_controller = BaseCrudController(
    model=SupermarketAreaIngredientComposite,
    api_model=supermarket_area_ingredinet_model,
    api_model_send=supermarket_area_ingredinet_model_send,
    use_caching=True,
    clear_cache_models=[Supermarket, SupermarketArea]
)


user_shared_edit_supermarket_controller = BaseCrudController(
    model=UserSharedEditSupermarket,
    api_model=supermarket_user_edit_model,
    api_model_send=supermarket_user_edit_model
)
