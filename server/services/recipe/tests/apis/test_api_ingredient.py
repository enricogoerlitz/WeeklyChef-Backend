# flake8: noqa
from server.core.models.db_models.ingredient import Ingredient
from server.db import db
from server.services.recipe.tests.apis.test_api_unit import create_unit


def create_ingredient(**data):
    data = data if data else {
        "name": "IngredientName",
        "displayname": "DisplayName",
        "default_price": 2.99,
        "quantity_per_unit": 2,
        "is_spices": False,
        "search_description": "SearchDescription",
        "unit_id": create_unit().id
    }
    obj = Ingredient(**data)

    db.session.add(obj)
    db.session.commit()

    return obj


# TEST GET


# TEST GET-LIST


# TEST-POST


# TEST UPDATE


# TEST DELETE
