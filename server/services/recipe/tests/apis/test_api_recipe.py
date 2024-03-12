# flake8: noqa
from server.core.models.db_models.recipe import Recipe
from server.services.recipe.tests.apis.test_api_category import create_category
from server.services.recipe.tests.utils import create_obj

# TODO: Implement Tests (use tag as template)

def create_recipe(creator_user_id):
    data = {
        "name": "RecipeName",
        "person_count": 2,
        "preperation_description": "PrepDescription",
        "preperation_time_minutes": 20,
        "difficulty": "einfach",
        "search_description": "SearchDescription",
        "creator_user_id": creator_user_id,
        "category_id": create_category().id
    }

    obj = Recipe(**data)
    return create_obj(obj)


def create_recipe_in_loop(num, creator_user_id, category):
    data = {
        "name": f"RecipeName{num}",
        "person_count": 2,
        "preperation_description": "PrepDescription",
        "preperation_time_minutes": 20,
        "difficulty": "einfach",
        "search_description": "SearchDescription",
        "creator_user_id": creator_user_id,
        "category_id": category.id
    }

    obj = Recipe(**data)
    return create_obj(obj)


# TEST GET


# TEST GET-LIST


# TEST-POST


# TEST UPDATE


# TEST DELETE
