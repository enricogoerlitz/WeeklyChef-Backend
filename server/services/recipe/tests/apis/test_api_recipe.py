# flake8: noqa
import json

from flask import Flask, testing

from server.core.models.db_models.recipe import (Recipe, RecipeIngredient, RecipeRating,
    RecipeTagComposite)
from server.services.recipe.tests.utils import create_obj
from server.core.models.db_models.user.user import User
from server.services.recipe.tests.apis.test_api_category import create_category
from server.services.recipe.tests.apis.test_api_tag import create_tag
from server.services.recipe.tests.apis.test_api_ingredient import create_ingredient
from server.services.recipe.tests.apis.test_api_unit import create_unit


ROUTE = "/api/v1/recipe"


def create_recipe(creator_user_id, category = None):
    data = {
        "name": "RecipeName",
        "person_count": 2,
        "preperation_description": "PrepDescription",
        "preperation_time_minutes": 20,
        "difficulty": "einfach",
        "search_description": "SearchDescription",
        "creator_user_id": creator_user_id,
        "category_id": category if category else create_category().id
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


def test_recipe_get(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        category = create_category()
        recipe = create_obj(
            Recipe(
                name="RecipeName",
                person_count=2,
                preperation_description="PrepDescription",
                preperation_time_minutes=20,
                difficulty="einfach",
                search_description="SearchDescription",
                creator_user_id=user.id,
                category_id=category.id
            )
        )
        api_route = f"{ROUTE}/{recipe.id}"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = recipe.to_dict()
        expected_data["category"] = category.to_dict()
        del expected_data["category_id"]

        # then
        assert response.status_code == 200
        assert result_data == expected_data


def test_recipe_get_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1"

        # when
        response = client.get(api_route, headers=headers)

        # then
        assert response.status_code == 404


def test_recipe_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        api_route = f"{ROUTE}/{recipe.id}"

        # when
        response_without = client.get(api_route)
        response_std = client.get(api_route, headers=std_headers)

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200


def test_recipe_get_rating(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        create_obj(
            RecipeRating(
                user_id=user.id,
                recipe_id=recipe.id,
                rating=3.0
            )
        )
        create_obj(
            RecipeRating(
                user_id=user_2.id,
                recipe_id=recipe.id,
                rating=5.0
            )
        )
        api_route = f"{ROUTE}/{recipe.id}/rating"

        # when
        response = client.get(api_route, headers=headers)
        resp_data = json.loads(response.data)
    
        # then
        assert response.status_code == 200
    
        assert resp_data["rating_avg"] == 4.0
        assert resp_data["rating_count"] == 2


# TEST GET-LIST


def test_recipe_get_list(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        COUNT = 3
        category = create_category()
        recipes = [create_recipe_in_loop(i, user.id, category) for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = [recipe.to_dict() for recipe in recipes]

        # then
        assert response.status_code == 200
        assert len(recipes) == COUNT
        assert result_data == expected_data


def test_recipe_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        COUNT = 3
        category = create_category()
        recipes = [create_recipe_in_loop(i, user.id, category) for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response_without = client.get(api_route)
        response_owner = client.get(api_route, headers=headers)
        response_other = client.get(api_route, headers=headers_2)

        result_owner_data = json.loads(response_owner.data)
        result_other_data = json.loads(response_other.data)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 200
        assert response_other.status_code == 200

        assert len(result_owner_data) == COUNT
        assert len(result_other_data) == COUNT


# TEST-POST


def test_recipe_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        category = create_category()
        data = {
            "name": "RecipeName",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Recipe.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()
        expected_data["creator_user_id"] = user.id

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_recipe_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        category = create_category()
        data = {
            "name": "RecipeName",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        api_route = f"{ROUTE}/"

        # when
        response_without = client.post(
            api_route, json=data)
        response_std = client.post(
            api_route, headers=headers, json=data)

        # then
        assert response_without.status_code != 201
        assert response_std.status_code == 201


def test_recipe_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        category = create_category()
        create_obj(
            Recipe(
                name="RecipeDuplicate",
                person_count=2,
                preperation_description="PrepDescription",
                preperation_time_minutes=30,
                difficulty="normal",
                search_description="SearchDescription",
                category_id=category.id,
                creator_user_id=user.id
            )
        )
        # given
        data_duplicate = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_name_is_null = {
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_name_to_short = {
            "name": "T" * 4,
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_name_to_long = {
            "name": "T" * 51,
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_person_count_is_null = {
            "name": "RecipeName",
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_person_count_to_low = {
            "name": "RecipeDuplicate",
            "person_count": 0,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_person_count_to_high = {
            "name": "RecipeDuplicate",
            "person_count": 101,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_prep_desc_is_null = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_prep_desc_to_short = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "T" * 4,
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_prep_desc_to_long = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "T" * 1001,
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_prep_time_min_is_null = {
            "name": "RecipeName",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_prep_time_min_to_low = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 0,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_prep_time_min_to_high = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 100_001,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_difficulty_is_null = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_difficulty_is_invalid = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "NO ALLOWED",
            "search_description": "SearchDescription",
            "category_id": category.id
        }
        data_search_desc_is_null = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "category_id": category.id
        }
        data_search_desc_to_short = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "T" * 3,
            "category_id": category.id
        }
        data_search_desc_to_long = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "T" * 76,
            "category_id": category.id
        }
        data_category_not_existing = {
            "name": "RecipeDuplicate",
            "person_count": 2,
            "preperation_description": "PrepDescription",
            "preperation_time_minutes": 30,
            "difficulty": "normal",
            "search_description": "SearchDescription",
            "category_id": -1
        }

        api_route = f"{ROUTE}/"

        # when
        resp_duplicate = client.post(api_route, headers=headers, json=data_duplicate)
        resp_name_is_null = client.post(api_route, headers=headers, json=data_name_is_null)
        resp_name_to_short = client.post(api_route, headers=headers, json=data_name_to_short)
        resp_name_to_long = client.post(api_route, headers=headers, json=data_name_to_long)
        resp_person_count_is_null = client.post(api_route, headers=headers, json=data_person_count_is_null)
        resp_person_count_to_low = client.post(api_route, headers=headers, json=data_person_count_to_low)
        resp_person_count_to_high = client.post(api_route, headers=headers, json=data_person_count_to_high)
        resp_prep_desc_is_null = client.post(api_route, headers=headers, json=data_prep_desc_is_null)
        resp_prep_desc_to_short = client.post(api_route, headers=headers, json=data_prep_desc_to_short)
        resp_prep_desc_to_long = client.post(api_route, headers=headers, json=data_prep_desc_to_long)
        resp_prep_time_min_is_null = client.post(api_route, headers=headers, json=data_prep_time_min_is_null)
        resp_prep_time_min_to_low = client.post(api_route, headers=headers, json=data_prep_time_min_to_low)
        resp_prep_time_min_to_high = client.post(api_route, headers=headers, json=data_prep_time_min_to_high)
        resp_difficulty_is_null = client.post(api_route, headers=headers, json=data_difficulty_is_null)
        resp_difficulty_is_invalid = client.post(api_route, headers=headers, json=data_difficulty_is_invalid)
        resp_search_desc_is_null = client.post(api_route, headers=headers, json=data_search_desc_is_null)
        resp_search_desc_to_short = client.post(api_route, headers=headers, json=data_search_desc_to_short)
        resp_search_desc_to_long = client.post(api_route, headers=headers, json=data_search_desc_to_long)
        resp_category_not_existing = client.post(api_route, headers=headers, json=data_category_not_existing)

        resp_duplicate_data = json.loads(resp_duplicate.data)
        resp_name_is_null_data = json.loads(resp_name_is_null.data)
        resp_name_to_short_data = json.loads(resp_name_to_short.data)
        resp_name_to_long_data = json.loads(resp_name_to_long.data)
        resp_person_count_is_null_data = json.loads(resp_person_count_is_null.data)
        resp_person_count_to_low_data = json.loads(resp_person_count_to_low.data)
        resp_person_count_to_high_data = json.loads(resp_person_count_to_high.data)
        resp_prep_desc_is_null_data = json.loads(resp_prep_desc_is_null.data)
        resp_prep_desc_to_short_data = json.loads(resp_prep_desc_to_short.data)
        resp_prep_desc_to_long_data = json.loads(resp_prep_desc_to_long.data)
        resp_prep_time_min_is_null_data = json.loads(resp_prep_time_min_is_null.data)
        resp_prep_time_min_to_low_data = json.loads(resp_prep_time_min_to_low.data)
        resp_prep_time_min_to_high_data = json.loads(resp_prep_time_min_to_high.data)
        resp_difficulty_is_null_data = json.loads(resp_difficulty_is_null.data)
        resp_difficulty_is_invalid_data = json.loads(resp_difficulty_is_invalid.data)
        resp_search_desc_is_null_data = json.loads(resp_search_desc_is_null.data)
        resp_search_desc_to_short_data = json.loads(resp_search_desc_to_short.data)
        resp_search_desc_to_long_data = json.loads(resp_search_desc_to_long.data)
        resp_category_not_existing_data = json.loads(resp_category_not_existing.data)

        # then
        assert resp_duplicate.status_code == 409
        assert resp_name_is_null.status_code == 400
        assert resp_name_to_short.status_code == 400
        assert resp_name_to_long.status_code == 400
        assert resp_person_count_is_null.status_code == 400
        assert resp_person_count_to_low.status_code == 400
        assert resp_person_count_to_high.status_code == 400
        assert resp_prep_desc_is_null.status_code == 400
        assert resp_prep_desc_to_short.status_code == 400
        assert resp_prep_desc_to_long.status_code == 400
        assert resp_prep_time_min_is_null.status_code == 400
        assert resp_prep_time_min_to_low.status_code == 400
        assert resp_prep_time_min_to_high.status_code == 400
        assert resp_difficulty_is_null.status_code == 400
        assert resp_difficulty_is_invalid.status_code == 400
        assert resp_search_desc_is_null.status_code == 400
        assert resp_search_desc_to_short.status_code == 400
        assert resp_search_desc_to_long.status_code == 400
        assert resp_category_not_existing.status_code == 404

        assert "message" in resp_duplicate_data
        assert "message" in resp_name_is_null_data
        assert "message" in resp_name_to_short_data
        assert "message" in resp_name_to_long_data
        assert "message" in resp_person_count_is_null_data
        assert "message" in resp_person_count_to_low_data
        assert "message" in resp_person_count_to_high_data
        assert "message" in resp_prep_desc_is_null_data
        assert "message" in resp_prep_desc_to_short_data
        assert "message" in resp_prep_desc_to_long_data
        assert "message" in resp_prep_time_min_is_null_data
        assert "message" in resp_prep_time_min_to_low_data
        assert "message" in resp_prep_time_min_to_high_data
        assert "message" in resp_difficulty_is_null_data
        assert "message" in resp_difficulty_is_invalid_data
        assert "message" in resp_search_desc_is_null_data
        assert "message" in resp_search_desc_to_short_data
        assert "message" in resp_search_desc_to_long_data
        assert "message" in resp_category_not_existing_data

        assert "name" in resp_duplicate_data["message"]
        assert "name" in resp_name_is_null_data["message"]
        assert "name" in resp_name_to_short_data["message"]
        assert "name" in resp_name_to_long_data["message"]
        assert "person_count" in resp_person_count_is_null_data["message"]
        assert "person_count" in resp_person_count_to_low_data["message"]
        assert "person_count" in resp_person_count_to_high_data["message"]
        assert "preperation_description" in resp_prep_desc_is_null_data["message"]
        assert "preperation_description" in resp_prep_desc_to_short_data["message"]
        assert "preperation_description" in resp_prep_desc_to_long_data["message"]
        assert "preperation_time_minutes" in resp_prep_time_min_is_null_data["message"]
        assert "preperation_time_minutes" in resp_prep_time_min_to_low_data["message"]
        assert "preperation_time_minutes" in resp_prep_time_min_to_high_data["message"]
        assert "difficulty" in resp_difficulty_is_null_data["message"]
        assert "difficulty" in resp_difficulty_is_invalid_data["message"]
        assert "search_description" in resp_search_desc_is_null_data["message"]
        assert "search_description" in resp_search_desc_to_short_data["message"]
        assert "search_description" in resp_search_desc_to_long_data["message"]
        assert "category" in resp_category_not_existing_data["message"]

        assert resp_difficulty_is_invalid_data["message"] == "The field 'difficulty' must be 'einfach', 'normal' or 'fortgeschritten''"


def test_recipe_tag_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        tag = create_tag("tag1")
        tag_2 = create_tag("tag2")

        api_route_1 = f"{ROUTE}/{recipe.id}/tag/{tag.id}"
        api_route_2 = f"{ROUTE}/{recipe.id}/tag/{tag_2.id}"

        # when
        response_1 = client.post(api_route_1, headers=headers)
        response_2 = client.post(api_route_2, headers=headers)

        resp_1_data = json.loads(response_1.data)
        resp_2_data = json.loads(response_2.data)

        # then
        assert response_1.status_code == 201
        assert response_2.status_code == 201

        assert resp_1_data == {"recipe_id": recipe.id, "tag_id": tag.id}
        assert resp_2_data =={"recipe_id": recipe.id, "tag_id": tag_2.id}


def test_recipe_ingredient_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        ingredient = create_ingredient()
        data = {"quantity": 5}

        api_route = f"{ROUTE}/{recipe.id}/ingredient/{ingredient.id}"

        # when
        response = client.post(api_route, headers=headers, json=data)

        resp_data = json.loads(response.data)

        # then
        assert response.status_code == 201

        assert resp_data == {
            "recipe_id": recipe.id,
            "ingredient_id": ingredient.id,
            "quantity": data["quantity"]
        }


def test_recipe_rating_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        data = {"rating": 3}

        api_route = f"{ROUTE}/{recipe.id}/rating"

        # when
        response = client.post(api_route, headers=headers, json=data)

        resp_data = json.loads(response.data)

        # then
        assert response.status_code == 201

        assert resp_data == {
            "recipe_id": recipe.id,
            "user_id": user.id,
            "rating": data["rating"]
        }

# TEST UPDATE


def test_recipe_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        data = {
            "name": "RecipeNameUpdate",
            "person_count": 3,
            "preperation_description": "PrepDescriptionUpdate",
            "preperation_time_minutes": 10,
            "difficulty": "fortgeschritten",
            "search_description": "SearchDescriptionUpdate"
        }
        api_route = f"{ROUTE}/{recipe.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Recipe.query.get(recipe.id).to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        del result_data_without_id["category_id"]
        del result_data_without_id["creator_user_id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 200
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_recipe_patch_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {"name": "NewRecipeName"}
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        # then
        assert response.status_code == 404


def test_recipe_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        recipe = create_recipe(user.id)

        data_without = {"name": "NewTestRecipe"}
        data_std = {"name": "NewTestRecipe2"}

        api_route = f"{ROUTE}/{recipe.id}"

        # when
        response_without = client.patch(
            api_route, json=data_without)
        response_owner = client.patch(
            api_route, headers=headers, json=data_std)
        response_other = client.patch(
            api_route, headers=headers_2, json=data_std)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 200
        assert response_other.status_code == 401


def test_recipe_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        category = create_category()
        recipe = create_obj(
            Recipe(
                name="RecipeName",
                person_count=2,
                preperation_description="PrepDescription",
                preperation_time_minutes=30,
                difficulty="normal",
                search_description="SearchDescription",
                category_id=category.id,
                creator_user_id=user.id
            )
        )
        create_obj(
            Recipe(
                name="RecipeDuplicate",
                person_count=2,
                preperation_description="PrepDescription",
                preperation_time_minutes=30,
                difficulty="normal",
                search_description="SearchDescription",
                category_id=category.id,
                creator_user_id=user.id
            )
        )
        # given
        data_duplicate = {"name": "RecipeDuplicate"}
        data_name_to_short = {"name": "T" * 4}
        data_name_to_long = {"name": "T" * 51}
        data_person_count_to_low = {"person_count": 0}
        data_person_count_to_high = {"person_count": 101}
        data_prep_desc_to_short = {"preperation_description": "T" * 4}
        data_prep_desc_to_long = {"preperation_description": "T" * 1001}
        data_prep_time_min_to_low = {"preperation_time_minutes": 0}
        data_prep_time_min_to_high = {"preperation_time_minutes": 100_001}
        data_difficulty_is_invalid = {"difficulty": "NO ALLOWED"}
        data_search_desc_to_short = {"search_description": "T" * 3}
        data_search_desc_to_long = {"search_description": "T" * 76}
        data_category_not_existing = {"category_id": -1}

        api_route = f"{ROUTE}/{recipe.id}"

        # when
        resp_duplicate = client.patch(api_route, headers=headers, json=data_duplicate)
        resp_name_to_short = client.patch(api_route, headers=headers, json=data_name_to_short)
        resp_name_to_long = client.patch(api_route, headers=headers, json=data_name_to_long)
        resp_person_count_to_low = client.patch(api_route, headers=headers, json=data_person_count_to_low)
        resp_person_count_to_high = client.patch(api_route, headers=headers, json=data_person_count_to_high)
        resp_prep_desc_to_short = client.patch(api_route, headers=headers, json=data_prep_desc_to_short)
        resp_prep_desc_to_long = client.patch(api_route, headers=headers, json=data_prep_desc_to_long)
        resp_prep_time_min_to_low = client.patch(api_route, headers=headers, json=data_prep_time_min_to_low)
        resp_prep_time_min_to_high = client.patch(api_route, headers=headers, json=data_prep_time_min_to_high)
        resp_difficulty_is_invalid = client.patch(api_route, headers=headers, json=data_difficulty_is_invalid)
        resp_search_desc_to_short = client.patch(api_route, headers=headers, json=data_search_desc_to_short)
        resp_search_desc_to_long = client.patch(api_route, headers=headers, json=data_search_desc_to_long)
        resp_category_not_existing = client.patch(api_route, headers=headers, json=data_category_not_existing)

        resp_duplicate_data = json.loads(resp_duplicate.data)
        resp_name_to_short_data = json.loads(resp_name_to_short.data)
        resp_name_to_long_data = json.loads(resp_name_to_long.data)
        resp_person_count_to_low_data = json.loads(resp_person_count_to_low.data)
        resp_person_count_to_high_data = json.loads(resp_person_count_to_high.data)
        resp_prep_desc_to_short_data = json.loads(resp_prep_desc_to_short.data)
        resp_prep_desc_to_long_data = json.loads(resp_prep_desc_to_long.data)
        resp_prep_time_min_to_low_data = json.loads(resp_prep_time_min_to_low.data)
        resp_prep_time_min_to_high_data = json.loads(resp_prep_time_min_to_high.data)
        resp_difficulty_is_invalid_data = json.loads(resp_difficulty_is_invalid.data)
        resp_search_desc_to_short_data = json.loads(resp_search_desc_to_short.data)
        resp_search_desc_to_long_data = json.loads(resp_search_desc_to_long.data)
        resp_category_not_existing_data = json.loads(resp_category_not_existing.data)

        # then
        assert resp_duplicate.status_code == 409
        assert resp_name_to_short.status_code == 400
        assert resp_name_to_long.status_code == 400
        assert resp_person_count_to_low.status_code == 400
        assert resp_person_count_to_high.status_code == 400
        assert resp_prep_desc_to_short.status_code == 400
        assert resp_prep_desc_to_long.status_code == 400
        assert resp_prep_time_min_to_low.status_code == 400
        assert resp_prep_time_min_to_high.status_code == 400
        assert resp_difficulty_is_invalid.status_code == 400
        assert resp_search_desc_to_short.status_code == 400
        assert resp_search_desc_to_long.status_code == 400
        assert resp_category_not_existing.status_code == 404

        assert "message" in resp_duplicate_data
        assert "message" in resp_name_to_short_data
        assert "message" in resp_name_to_long_data
        assert "message" in resp_person_count_to_low_data
        assert "message" in resp_person_count_to_high_data
        assert "message" in resp_prep_desc_to_short_data
        assert "message" in resp_prep_desc_to_long_data
        assert "message" in resp_prep_time_min_to_low_data
        assert "message" in resp_prep_time_min_to_high_data
        assert "message" in resp_difficulty_is_invalid_data
        assert "message" in resp_search_desc_to_short_data
        assert "message" in resp_search_desc_to_long_data
        assert "message" in resp_category_not_existing_data

        assert "name" in resp_duplicate_data["message"]
        assert "name" in resp_name_to_short_data["message"]
        assert "name" in resp_name_to_long_data["message"]
        assert "person_count" in resp_person_count_to_low_data["message"]
        assert "person_count" in resp_person_count_to_high_data["message"]
        assert "preperation_description" in resp_prep_desc_to_short_data["message"]
        assert "preperation_description" in resp_prep_desc_to_long_data["message"]
        assert "preperation_time_minutes" in resp_prep_time_min_to_low_data["message"]
        assert "preperation_time_minutes" in resp_prep_time_min_to_high_data["message"]
        assert "difficulty" in resp_difficulty_is_invalid_data["message"]
        assert "search_description" in resp_search_desc_to_short_data["message"]
        assert "search_description" in resp_search_desc_to_long_data["message"]
        assert "category" in resp_category_not_existing_data["message"]

        assert resp_difficulty_is_invalid_data["message"] == "The field 'difficulty' must be 'einfach', 'normal' or 'fortgeschritten''"


def test_recipe_ingredient_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        ingredient = create_ingredient()
        create_obj(
            RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=5
            )
        )
        data = {"quantity": 90}

        api_route = f"{ROUTE}/{recipe.id}/ingredient/{ingredient.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        resp_data = json.loads(response.data)

        # then
        assert response.status_code == 200

        assert resp_data["quantity"] == data["quantity"]


def test_recipe_rating_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        create_obj(
            RecipeRating(
                recipe_id=recipe.id,
                user_id=user.id,
                rating=1.5
            )
        )
        data = {"rating": 3}

        api_route = f"{ROUTE}/{recipe.id}/rating"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        resp_data = json.loads(response.data)

        # then
        assert response.status_code == 200

        assert resp_data["rating"] == data["rating"]


# TEST DELETE


def test_recipe_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        db_model_count_before = Recipe.query.count()
        api_route = f"{ROUTE}/{recipe.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = Recipe.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_recipe_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        create_recipe(user.id)
        db_model_count_before = Recipe.query.count()
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = Recipe.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_recipe_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        recipe = create_recipe(user.id)

        api_route = f"{ROUTE}/{recipe.id}"

        # when
        response_without = client.delete(api_route)
        response_other = client.delete(api_route, headers=headers_2)
        response_owner = client.delete(api_route, headers=headers)

        # then
        assert response_without.status_code != 204
        assert response_owner.status_code == 204
        assert response_other.status_code == 401


def test_recipe_tag_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        tag = create_tag()
        create_obj(
            RecipeTagComposite(
                recipe_id=recipe.id,
                tag_id=tag.id
            )
        )
        db_model_count_before = RecipeTagComposite.query.count()
        api_route = f"{ROUTE}/{recipe.id}/tag/{tag.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = RecipeTagComposite.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0
    

def test_recipe_ingredient_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        ingredient = create_ingredient()
        create_obj(
            RecipeIngredient(
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=3
            )
        )
        db_model_count_before = RecipeIngredient.query.count()
        api_route = f"{ROUTE}/{recipe.id}/ingredient/{ingredient.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = RecipeIngredient.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_recipe_rating_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        recipe = create_recipe(user.id)
        create_obj(
            RecipeRating(
                recipe_id=recipe.id,
                user_id=user.id,
                rating=4.
            )
        )
        db_model_count_before = RecipeRating.query.count()
        api_route = f"{ROUTE}/{recipe.id}/rating"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = RecipeRating.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0
