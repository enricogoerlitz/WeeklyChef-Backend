# flake8: noqa
import json

from flask import Flask, testing

from server.db import db
from server.services.recipe.tests.apis.test_api_unit import create_unit
from server.core.models.db_models.ingredient import Ingredient
from server.core.models.db_models.unit import Unit


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


def create_ingredient_dict(unit: Unit):
    data = {
        "name": "IngredientName",
        "displayname": "DisplayName",
        "default_price": 2.99,
        "quantity_per_unit": 2,
        "is_spices": False,
        "search_description": "SearchDescription",
        "unit_id": unit.id
    }
    return data


def create_ingredient_loop(num: int, unit: Unit):
    data = {
        "name": f"IngredientName{num}",
        "displayname": "DisplayName",
        "default_price": 2.99,
        "quantity_per_unit": 2,
        "is_spices": False,
        "search_description": "SearchDescription",
        "unit_id": unit.id
    }
    obj = Ingredient(**data)

    db.session.add(obj)
    db.session.commit()

    return obj


def create_ingredient_dict_loop(num: int, unit: Unit):
    data = {
        "name": f"IngredientName{num}",
        "displayname": "DisplayName",
        "default_price": 2.99,
        "quantity_per_unit": 2,
        "is_spices": False,
        "search_description": "SearchDescription",
        "unit_id": unit.id
    }
    return data


ROUTE = "/api/v1/ingredient"


# TEST GET


def test_ingredient_get(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        ingredient = create_ingredient()
        api_route = f"{ROUTE}/{ingredient.id}"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = ingredient.to_dict()
        expected_data["unit"] = Unit.query.get(expected_data["unit_id"]).to_dict()
        del expected_data["unit_id"]

        # then
        print(response, result_data)
        assert response.status_code == 200
        assert result_data == expected_data


def test_ingredient_get_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1"

        # when
        response = client.get(api_route, headers=admin_headers)

        # then
        assert response.status_code == 404


def test_ingredient_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        ingredient = create_ingredient()
        api_route = f"{ROUTE}/{ingredient.id}"

        # when
        response_without = client.get(api_route)
        response_std = client.get(api_route, headers=std_headers)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = ingredient.to_dict()
        expected_data["unit"] = Unit.query.get(expected_data["unit_id"]).to_dict()
        del expected_data["unit_id"]

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST GET-LIST


def test_ingredient_get_list(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        COUNT = 3
        unit = create_unit()
        ingredients = [create_ingredient_loop(i, unit) for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = [ingredient.to_dict() for ingredient in ingredients]

        for data in expected_data:
            data["unit"] = unit.to_dict()
            del data["unit_id"]

        # then
        assert response.status_code == 200
        assert len(result_data) == len(expected_data)
        for i in range(0, len(expected_data)):
            assert result_data[i] == expected_data[i]


def test_ingredient_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        COUNT = 3
        unit = create_unit()
        ingredients = [create_ingredient_loop(i, unit) for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response_without = client.get(api_route)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)
        response_std = client.get(api_route, headers=std_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = [ingredient.to_dict() for ingredient in ingredients]

        for data in expected_data:
            data["unit"] = unit.to_dict()
            del data["unit_id"]

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST-POST


def test_ingredient_post(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        data = {
            "name": "IngredientName",
            "displayname": "DisplayName",
            "default_price": 2.49,
            "quantity_per_unit": 200,
            "is_spices": False,
            "search_description": "SearchDescription",
            "unit_id": unit.id
        }
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()
        del expected_data["unit_id"]
        expected_data["unit"] = unit.to_dict()

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data


def test_ingredient_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        ingredients = [create_ingredient_dict_loop(i, unit) for i in range(0, 4)]

        data_without = ingredients[3]
        data_std = ingredients[0]
        data_staff = ingredients[1]
        data_admin = ingredients[2]
        api_route = f"{ROUTE}/"

        print(data_std)
        # when
        response_without = client.post(
            api_route, json=data_without)
        response_std = client.post(
            api_route, headers=std_headers, json=data_std)
        response_staff = client.post(
            api_route, headers=staff_headers, json=data_staff)
        response_admin = client.post(
            api_route, headers=admin_headers, json=data_admin)

        # then
        assert response_without.status_code != 201
        assert response_staff.status_code == 201
        assert response_std.status_code == 201
        assert response_admin.status_code == 201


def test_ingredient_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        default_ingredient = create_ingredient_dict(unit)
        data_name_is_null = default_ingredient.copy()
        data_name_is_to_short = default_ingredient.copy()
        data_name_is_to_long = default_ingredient.copy()

        data_displayname_is_null = default_ingredient.copy()
        data_displayname_is_to_short = default_ingredient.copy()
        data_displayname_is_to_long = default_ingredient.copy()

        data_default_price_is_null = default_ingredient.copy()
        data_default_price_is_to_low = default_ingredient.copy()

        data_quantity_per_unit_is_null = default_ingredient.copy()
        data_quantity_per_unit_is_to_low = default_ingredient.copy()

        data_quantity_is_spices_is_null = default_ingredient.copy()

        data_search_description_is_null = default_ingredient.copy()
        data_search_description_is_to_short = default_ingredient.copy()
        data_search_description_is_to_long = default_ingredient.copy()

        data_unit_id_is_null = default_ingredient.copy()
        data_unit_id_is_not_existing = default_ingredient.copy()

        del data_name_is_null["name"]
        data_name_is_to_short["name"] = "T" * 3
        data_name_is_to_long["name"] = "T" * 51

        del data_displayname_is_null["displayname"]
        data_displayname_is_to_short["displayname"] = "T" * 2
        data_displayname_is_to_long["displayname"] = "T" * 26

        del data_default_price_is_null["default_price"]
        data_default_price_is_to_low["default_price"] = -1

        del data_quantity_per_unit_is_null["quantity_per_unit"]
        data_quantity_per_unit_is_to_low["quantity_per_unit"] = -1

        del data_quantity_is_spices_is_null["is_spices"]

        del data_search_description_is_null["search_description"]
        data_search_description_is_to_short["search_description"] = "T" * 3
        data_search_description_is_to_long["search_description"] = "T" * 76

        del data_unit_id_is_null["unit_id"]
        data_unit_id_is_not_existing["unit_id"] = -1

        api_route = f"{ROUTE}/"

        # when
        resp_name_is_null = client.post(
            api_route, headers=admin_headers, json=data_name_is_null)
        resp_name_is_to_short = client.post(
            api_route, headers=admin_headers, json=data_name_is_to_short)
        resp_name_is_to_long = client.post(
            api_route, headers=admin_headers, json=data_name_is_to_long)
        resp_displayname_is_null = client.post(
            api_route, headers=admin_headers, json=data_displayname_is_null)
        resp_displayname_is_to_short = client.post(
            api_route, headers=admin_headers, json=data_displayname_is_to_short)
        resp_displayname_is_to_long = client.post(
            api_route, headers=admin_headers, json=data_displayname_is_to_long)
        resp_default_price_is_null = client.post(
            api_route, headers=admin_headers, json=data_default_price_is_null)
        resp_default_price_is_to_low = client.post(
            api_route, headers=admin_headers, json=data_default_price_is_to_low)
        resp_quantity_per_unit_is_null = client.post(
            api_route, headers=admin_headers, json=data_quantity_per_unit_is_null)
        resp_quantity_per_unit_is_to_low = client.post(
            api_route, headers=admin_headers, json=data_quantity_per_unit_is_to_low)
        resp_quantity_is_spices_is_null = client.post(
            api_route, headers=admin_headers, json=data_quantity_is_spices_is_null)
        resp_search_description_is_null = client.post(
            api_route, headers=admin_headers, json=data_search_description_is_null)
        resp_search_description_is_to_short = client.post(
            api_route, headers=admin_headers, json=data_search_description_is_to_short)
        resp_search_description_is_to_long = client.post(
            api_route, headers=admin_headers, json=data_search_description_is_to_long)
        resp_unit_id_is_null = client.post(
            api_route, headers=admin_headers, json=data_unit_id_is_null)
        resp_unit_id_is_not_existing = client.post(
            api_route, headers=admin_headers, json=data_unit_id_is_not_existing)

        resp_name_is_null_data = json.loads(resp_name_is_null.data)
        resp_name_is_to_short_data = json.loads(resp_name_is_to_short.data)
        resp_name_is_to_long_data = json.loads(resp_name_is_to_long.data)
        resp_displayname_is_null_data = json.loads(resp_displayname_is_null.data)
        resp_displayname_is_to_short_data = json.loads(resp_displayname_is_to_short.data)
        resp_displayname_is_to_long_data = json.loads(resp_displayname_is_to_long.data)
        resp_default_price_is_null_data = json.loads(resp_default_price_is_null.data)
        resp_default_price_is_to_low_data = json.loads(resp_default_price_is_to_low.data)
        resp_quantity_per_unit_is_null_data = json.loads(resp_quantity_per_unit_is_null.data)
        resp_quantity_per_unit_is_to_low_data = json.loads(resp_quantity_per_unit_is_to_low.data)
        resp_quantity_is_spices_is_null_data = json.loads(resp_quantity_is_spices_is_null.data)
        resp_search_description_is_null_data = json.loads(resp_search_description_is_null.data)
        resp_search_description_is_to_short_data = json.loads(resp_search_description_is_to_short.data)
        resp_search_description_is_to_long_data = json.loads(resp_search_description_is_to_long.data)
        resp_unit_id_is_null_data = json.loads(resp_unit_id_is_null.data)
        resp_unit_id_is_not_existing_data = json.loads(resp_unit_id_is_not_existing.data)

        # then
        assert resp_name_is_null.status_code == 400
        assert resp_name_is_to_short.status_code == 400
        assert resp_name_is_to_long.status_code == 400
        assert resp_displayname_is_null.status_code == 400
        assert resp_displayname_is_to_short.status_code == 400
        assert resp_displayname_is_to_long.status_code == 400
        assert resp_default_price_is_null.status_code == 400
        assert resp_default_price_is_to_low.status_code == 400
        assert resp_quantity_per_unit_is_null.status_code == 400
        assert resp_quantity_per_unit_is_to_low.status_code == 400
        assert resp_quantity_is_spices_is_null.status_code == 400
        assert resp_search_description_is_null.status_code == 400
        assert resp_search_description_is_to_short.status_code == 400
        assert resp_search_description_is_to_long.status_code == 400
        assert resp_unit_id_is_null.status_code == 400
        assert resp_unit_id_is_not_existing.status_code == 404

        assert "message" in resp_name_is_null_data
        assert "message" in resp_name_is_to_short_data
        assert "message" in resp_name_is_to_long_data
        assert "message" in resp_displayname_is_null_data
        assert "message" in resp_displayname_is_to_short_data
        assert "message" in resp_displayname_is_to_long_data
        assert "message" in resp_default_price_is_null_data
        assert "message" in resp_default_price_is_to_low_data
        assert "message" in resp_quantity_per_unit_is_null_data
        assert "message" in resp_quantity_per_unit_is_to_low_data
        assert "message" in resp_quantity_is_spices_is_null_data
        assert "message" in resp_search_description_is_null_data
        assert "message" in resp_search_description_is_to_short_data
        assert "message" in resp_search_description_is_to_long_data
        assert "message" in resp_unit_id_is_null_data
        assert "message" in resp_unit_id_is_not_existing_data

        assert "name" in resp_name_is_null_data["message"]
        assert "name" in resp_name_is_to_short_data["message"]
        assert "name" in resp_name_is_to_long_data["message"]
        assert "displayname" in resp_displayname_is_null_data["message"]
        assert "displayname" in resp_displayname_is_to_short_data["message"]
        assert "displayname" in resp_displayname_is_to_long_data["message"]
        assert "default_price" in resp_default_price_is_null_data["message"]
        assert "default_price" in resp_default_price_is_to_low_data["message"]
        assert "quantity_per_unit" in resp_quantity_per_unit_is_null_data["message"]
        assert "quantity_per_unit" in resp_quantity_per_unit_is_to_low_data["message"]
        assert "is_spices" in resp_quantity_is_spices_is_null_data["message"]
        assert "search_description" in resp_search_description_is_null_data["message"]
        assert "search_description" in resp_search_description_is_to_short_data["message"]
        assert "search_description" in resp_search_description_is_to_long_data["message"]
        assert "unit_id" in resp_unit_id_is_null_data["message"]
        assert "unit_id" in resp_unit_id_is_not_existing_data["message"]


# TEST UPDATE


def test_ingredient_patch(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        ingredient_original = create_ingredient()
        upadte_data = {
            "name": "IngredientNameChanged",
            "displayname": "DisplayNameChanged",
            "default_price": 3.49,
            "quantity_per_unit": 300,
            "is_spices": True,
            "search_description": "SearchDescriptionChanged"
        }
        api_route = f"{ROUTE}/{ingredient_original.id}"

        # when
        response = client.patch(api_route, headers=admin_headers, json=upadte_data)

        result_data_db = Ingredient.query.get(ingredient_original.id).to_dict()

        # then
        assert response.status_code == 200
        assert ingredient_original.to_dict() == result_data_db


def test_ingredient_patch_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        data = {}
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        # then
        assert response.status_code == 404


def test_ingredient_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        ingredient = create_ingredient()

        data_without = {"name": "NewTestIngredient"}
        data_std = {"name": "NewTestIngredient2"}
        data_staff = {"name": "NewTestIngredient3"}
        data_admin = {"name": "NewTestIngredient4"}

        api_route = f"{ROUTE}/{ingredient.id}"

        # when
        response_without = client.patch(
            api_route, json=data_without)
        response_std = client.patch(
            api_route, headers=std_headers, json=data_std)
        response_staff = client.patch(
            api_route, headers=staff_headers, json=data_staff)
        response_admin = client.patch(
            api_route, headers=admin_headers, json=data_admin)

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 401
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200


def test_ingredient_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        ingredient = create_ingredient()

        data_name_duplicate = {"name": ingredient.name}
        data_name_to_long = {"name": "T" * 51}
        api_route = f"{ROUTE}/{ingredient.id}"

        # when
        response_name_duplicate = client.patch(
            api_route, headers=admin_headers, json=data_name_duplicate)
        response_name_to_long = client.patch(
            api_route, headers=admin_headers, json=data_name_to_long)

        response_name_duplicate_data = json.loads(response_name_duplicate.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_duplicate.status_code == 409
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_duplicate_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_duplicate_data["message"]
        assert "name" in response_name_to_long_data["message"]


# TEST DELETE


def test_ingredient_delete(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        ingredient = create_ingredient()
        db_model_count_before = Ingredient.query.count()
        api_route = f"{ROUTE}/{ingredient.id}"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = Ingredient.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_ingredient_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        create_ingredient()
        db_model_count_before = Ingredient.query.count()
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = Ingredient.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_ingredient_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        ingredients = [create_ingredient_dict_loop(i, unit) for i in range(0, 4)]

        ingredient_without = create_ingredient(**ingredients[3])
        ingredient_std = create_ingredient(**ingredients[0])
        ingredient_staff = create_ingredient(**ingredients[1])
        ingredient_admin = create_ingredient(**ingredients[2])

        api_route_without = f"{ROUTE}/{ingredient_without.id}"
        api_route_std = f"{ROUTE}/{ingredient_std.id}"
        api_route_staff = f"{ROUTE}/{ingredient_staff.id}"
        api_route_admin = f"{ROUTE}/{ingredient_admin.id}"

        # when
        response_without = client.delete(api_route_without)
        response_std = client.delete(api_route_std, headers=std_headers)
        response_staff = client.delete(api_route_staff, headers=staff_headers)
        response_admin = client.delete(api_route_admin, headers=admin_headers)

        result_data_db_without = Ingredient.query.get(ingredient_without.id)
        result_data_db_std = Ingredient.query.get(ingredient_std.id)
        result_data_db_staff = Ingredient.query.get(ingredient_staff.id)
        result_data_db_admin = Ingredient.query.get(ingredient_admin.id)

        # then
        assert response_without.status_code != 204
        assert response_std.status_code == 401
        assert response_staff.status_code == 204
        assert response_admin.status_code == 204

        assert result_data_db_without is not None
        assert result_data_db_std is not None
        assert result_data_db_staff is None
        assert result_data_db_admin is None
