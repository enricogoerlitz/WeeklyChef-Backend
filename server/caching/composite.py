"""
IN DEV, JUST AN IDEA
"""

from enum import Enum
from abc import ABC, abstractclassmethod
from typing import Type

from flask_restx import Model

from server.caching import redis
from server.core.models.db_models.planner import (
    RecipePlanner, RecipePlannerItem
)
from server.core.models.db_models.unit import Unit
from server.core.models.db_models.tag import Tag
from server.core.models.db_models.category import Category
from server.core.models.db_models.ingredient import Ingredient
from server.core.models.db_models.recipe import Recipe, RecipeIngredient
from server.core.models.db_models.collection import (
    Collection, CollectionRecipeComposite
)
from server.core.models.db_models.cart import Cart, CartItem
from server.core.models.db_models.supermarket import (
    SupermarketArea,
    SupermarketAreaIngredientComposite)


class CachingComponentType(Enum):
    MODEL = 1
    COMPOSITE = 2


class AbstractCachingComponent(ABC):

    @abstractclassmethod
    def set_parent(self, parent: 'CachingModelComposite') -> None: pass

    @abstractclassmethod
    def reset_cache(self) -> None: pass

    @abstractclassmethod
    def get_type(self) -> CachingComponentType: pass


class CachingModel(AbstractCachingComponent):
    _parent: 'CachingModelComposite' = None

    def __init__(
            self,
            model: Type[Model]
    ) -> None:
        self._model = model

    def get_type(self) -> CachingComponentType:
        return CachingComponentType.MODEL

    def set_parent(self, parent: 'CachingModelComposite') -> None:
        self._parent = parent

    def reset_cache(self) -> None:
        redis_key_pattern = redis.gen_key(self._model, "*")
        redis.clear_cache(redis_key_pattern)
        print(f"{str(self)}: RESET MODEL CACHE: {redis_key_pattern}")

    def __str__(self) -> str:
        return f"CachingModel(model={self._model.__name__})"

    def __repr__(self) -> str:
        return str(self)


class CachingModelComposite(AbstractCachingComponent):

    def __init__(
            self,
            components: list[AbstractCachingComponent] = None,
            is_root: bool = False
    ) -> None:
        self._is_root = is_root

        self._components = components if components is not None else []
        for child in self._components:
            child.set_parent(self)

    def get_type(self) -> CachingComponentType:
        return CachingComponentType.COMPOSITE

    def add(self, component: AbstractCachingComponent) -> None:
        self._components.append(component)
        component.set_parent(self)

    def remove(self, component: AbstractCachingComponent) -> None:
        self._components.remove(component)

    def get_children(self) -> list[Model]:
        return self._components

    def reset_cache(self, reset_this_level: bool = False) -> None:
        print(f"{str(self)}: RESET CACHE OF CHILDREN")
        for child in self._components:
            is_reset = (
                reset_this_level or
                child.get_type() == CachingComponentType.COMPOSITE
            )

            if not is_reset:
                continue

            child.reset_cache(reset_this_level=True)

    def print_recursive(self) -> None:
        self_str = f"CachingModelComposite(\nchildren={str(self._models)})"
        print(self_str)

    def _set_index(self) -> None:
        # TODO SETUP INDEX!
        pass


if __name__ == "__main__":

    # CACHING MODELS

    unit_caching_model = CachingModel(Unit)
    tag_caching_model = CachingModel(Tag)
    category_caching_model = CachingModel(Category)

    ingredient_caching_model = CachingModel(Ingredient)
    recipe_ingredient_caching_model = CachingModel(RecipeIngredient)
    recipe_caching_model = CachingModel(Recipe)

    supermarket_area_caching_model = CachingModel(SupermarketArea)
    supermarket_area_ingredient_caching_model = CachingModel(
        SupermarketAreaIngredientComposite)

    recipe_planner_caching_model = CachingModel(RecipePlanner)
    recipe_planner_item_caching_model = CachingModel(RecipePlannerItem)

    collection_caching_model = CachingModel(Collection)
    collection_recipe_caching_model = CachingModel(CollectionRecipeComposite)

    cart_caching_model = CachingModel(Cart)
    cart_item_caching_model = CachingModel(CartItem)

    # COMPOSITE MODELS

    recipe_centered_composite = CachingModelComposite([
        CachingModel(Unit),
        CachingModel(Tag),
        CachingModel(Category),
        CachingModelComposite([
            CachingModel(Ingredient),
            CachingModel(RecipeIngredient),
            CachingModelComposite([
                CachingModel(Recipe),
                CachingModelComposite([
                    CachingModel(CollectionRecipeComposite),
                    CachingModelComposite([
                        CachingModel(Collection),
                    ]),
                ]),
            ])
        ])
    ], is_root=True)

    cart_composite = CachingModelComposite([
        CachingModel(Ingredient),
        CachingModel(RecipeIngredient),
        CachingModelComposite([
            CachingModel(Recipe),
        ])
    ], is_root=True)

    recipe_service_components = CachingModelComposite([
        CachingModel(Unit),
        CachingModel(Tag),
        CachingModel(Category),
        CachingModelComposite([
            CachingModel(Ingredient),
            CachingModelComposite([
                CachingModel(SupermarketAreaIngredientComposite),
                CachingModel(SupermarketArea),

                # SUPERMARKET
                CachingModelComposite([
                    CachingModel(RecipePlannerItem),
                    CachingModelComposite([
                        CachingModel(RecipePlanner)
                    ])
                ]),
            ]),
        ]),

        CachingModelComposite([
            CachingModel(Ingredient),
            CachingModel(RecipeIngredient),

            # RECIPE
            CachingModelComposite([
                CachingModel(Recipe),

                # COLLECTION
                CachingModelComposite([
                    CachingModel(CollectionRecipeComposite),
                    CachingModelComposite([
                        CachingModel(Collection),
                    ]),
                ]),

                # PLANNER
                CachingModelComposite([
                    CachingModel(RecipePlannerItem),
                    CachingModelComposite([
                        CachingModel(RecipePlanner)
                    ])
                ]),

                # CART
                CachingModelComposite([
                    CachingModel(CartItem),
                    CachingModelComposite([
                        CachingModel(Cart)
                    ])
                ])
            ])
        ])
    ])

    # AM ENDE EIN DICTIONARY BAUEN, WLECHE MIT GET.RESET AREBIET!
    cart_model = None
    supermarket_model = None
