# flake8: noqa
import json

from flask import Flask, testing
from server.core.models.db_models.cart import Cart, CartItem
from server.core.models.db_models.user.user import User
from server.services.recipe.tests.apis.test_api_ingredient import (
    create_ingredient
)
from server.services.recipe.tests.apis.test_api_recipe import create_recipe
from server.services.recipe.tests.utils import create_obj


ROUTE = "/api/v1/cart"

# TEST GET


#   CART


def test_cart_get(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name="CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        cart_item = create_obj(
            CartItem(
                cart_id=cart.id,
                recipe_id=create_recipe(user.id).id,
                ingredient_id=create_ingredient().id,
                quantity=2,
                is_done=False
            )
        )
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = cart.to_dict()
        expected_data_item = cart_item.to_dict()
        expected_data["items"] = [expected_data_item]

        # then
        assert response.status_code == 200

        assert result_data["name"] == expected_data["name"]
        assert result_data["owner_user_id"] == expected_data["owner_user_id"]
        assert result_data["is_active"] == expected_data["is_active"]
        assert len(result_data["items"]) == len(expected_data["items"])
        assert result_data["items"][0]["cart_id"] == expected_data_item["cart_id"]
        assert result_data["items"][0]["recipe"]["id"] == expected_data_item["recipe_id"]
        assert result_data["items"][0]["ingredient"]["id"] == expected_data_item["ingredient_id"]
        assert result_data["items"][0]["quantity"] == expected_data_item["quantity"]
        assert result_data["items"][0]["is_done"] == expected_data_item["is_done"]


"""

def test_cart_get_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1"

        # when
        response = client.get(api_route, headers=admin_headers)

        # then
        assert response.status_code == 404


def test_cart_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response_without = client.get(api_route)
        response_std = client.get(api_route, headers=std_headers)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = cart.to_dict()

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


def test_cart_get_clear(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = cart.to_dict()

        # then
        assert response.status_code == 200
        assert result_data == expected_data


def test_cart_get_clear_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1"

        # when
        response = client.get(api_route, headers=admin_headers)

        # then
        assert response.status_code == 404


def test_cart_get_clear_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response_without = client.get(api_route)
        response_std = client.get(api_route, headers=std_headers)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = cart.to_dict()

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST GET-LIST

#   CART

def test_cart_get_list(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        COUNT = 3
        carts = [create_cart_with_relations(f"cart{i}") for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = [cart.to_dict() for cart in carts]

        # then
        assert response.status_code == 200
        assert len(carts) == COUNT
        assert result_data == expected_data


def test_cart_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        COUNT = 3
        carts = [create_cart_with_relations(f"cart{i}") for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response_without = client.get(api_route)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)
        response_std = client.get(api_route, headers=std_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = [cart.to_dict() for cart in carts]

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST-POST

def test_cart_post(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data = {"name": "Testcart"}
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = cart.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_cart_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data_without = {"name": "Testcart"}
        data_std = {"name": "Testcart2"}
        data_staff = {"name": "Testcart3"}
        data_admin = {"name": "Testcart4"}
        api_route = f"{ROUTE}/"

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
        assert response_std.status_code == 401
        assert response_staff.status_code == 201
        assert response_admin.status_code == 201


def test_cart_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data_name_is_null = {}                  # "name" not given
        data_name_to_short = {"name": "T" * 3}  # min 4
        data_name_to_long = {"name": "T" * 31}  # max 30
        api_route = f"{ROUTE}/"

        # when
        response_name_is_null = client.post(
            api_route, headers=admin_headers, json=data_name_is_null)
        response_name_to_short = client.post(
            api_route, headers=admin_headers, json=data_name_to_short)
        response_name_to_long = client.post(
            api_route, headers=admin_headers, json=data_name_to_long)

        response_name_is_null_data = json.loads(response_name_is_null.data)
        response_name_to_short_data = json.loads(response_name_to_short.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_is_null.status_code == 400
        assert response_name_to_short.status_code == 400
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_is_null_data
        assert "message" in response_name_to_short_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_is_null_data["message"]
        assert "name" in response_name_to_short_data["message"]
        assert "name" in response_name_to_long_data["message"]


#   CART ITEM

def test_cart_item_post(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data = {"name": "Testcart"}
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = cart.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_cart_item_post_invalid_id(): pass


def test_cart_item_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data_without = {"name": "Testcart"}
        data_std = {"name": "Testcart2"}
        data_staff = {"name": "Testcart3"}
        data_admin = {"name": "Testcart4"}
        api_route = f"{ROUTE}/"

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
        assert response_std.status_code == 401
        assert response_staff.status_code == 201
        assert response_admin.status_code == 201


def test_cart_item_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data_name_is_null = {}                  # "name" not given
        data_name_to_short = {"name": "T" * 3}  # min 4
        data_name_to_long = {"name": "T" * 31}  # max 30
        api_route = f"{ROUTE}/"

        # when
        response_name_is_null = client.post(
            api_route, headers=admin_headers, json=data_name_is_null)
        response_name_to_short = client.post(
            api_route, headers=admin_headers, json=data_name_to_short)
        response_name_to_long = client.post(
            api_route, headers=admin_headers, json=data_name_to_long)

        response_name_is_null_data = json.loads(response_name_is_null.data)
        response_name_to_short_data = json.loads(response_name_to_short.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_is_null.status_code == 400
        assert response_name_to_short.status_code == 400
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_is_null_data
        assert "message" in response_name_to_short_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_is_null_data["message"]
        assert "name" in response_name_to_short_data["message"]
        assert "name" in response_name_to_long_data["message"]


#   SHARED USER

def test_cart_shared_user_post(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data = {"name": "Testcart"}
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = cart.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_cart_shared_user_post_invalid_id(): pass


def test_cart_shared_user_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data_without = {"name": "Testcart"}
        data_std = {"name": "Testcart2"}
        data_staff = {"name": "Testcart3"}
        data_admin = {"name": "Testcart4"}
        api_route = f"{ROUTE}/"

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
        assert response_std.status_code == 401
        assert response_staff.status_code == 201
        assert response_admin.status_code == 201


def test_cart_shared_user_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data_name_is_null = {}                  # "name" not given
        data_name_to_short = {"name": "T" * 3}  # min 4
        data_name_to_long = {"name": "T" * 31}  # max 30
        api_route = f"{ROUTE}/"

        # when
        response_name_is_null = client.post(
            api_route, headers=admin_headers, json=data_name_is_null)
        response_name_to_short = client.post(
            api_route, headers=admin_headers, json=data_name_to_short)
        response_name_to_long = client.post(
            api_route, headers=admin_headers, json=data_name_to_long)

        response_name_is_null_data = json.loads(response_name_is_null.data)
        response_name_to_short_data = json.loads(response_name_to_short.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_is_null.status_code == 400
        assert response_name_to_short.status_code == 400
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_is_null_data
        assert "message" in response_name_to_short_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_is_null_data["message"]
        assert "name" in response_name_to_short_data["message"]
        assert "name" in response_name_to_long_data["message"]


# TEST UPDATE

#   CART

def test_cart_patch(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        data = {"name": "NewcartName"}
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = cart.query.get(cart.id).to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 200
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_cart_patch_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        data = {"name": "NewcartName"}
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        # then
        assert response.status_code == 404


def test_cart_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        cart = create_cart_with_relations()

        data_without = {"name": "NewTestcart"}
        data_std = {"name": "NewTestcart2"}
        data_staff = {"name": "NewTestcart3"}
        data_admin = {"name": "NewTestcart4"}

        api_route = f"{ROUTE}/{cart.id}"

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


def test_cart_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        cart = create_cart_with_relations()

        data_name_to_short = {"name": "T" * 3}  # min 4
        data_name_to_long = {"name": "T" * 31}  # max 30
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response_name_to_short = client.patch(
            api_route, headers=admin_headers, json=data_name_to_short)
        response_name_to_long = client.patch(
            api_route, headers=admin_headers, json=data_name_to_long)

        response_name_to_short_data = json.loads(response_name_to_short.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_to_short.status_code == 400
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_to_short_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_to_short_data["message"]
        assert "name" in response_name_to_long_data["message"]


#   CART ITEM

def test_cart_item_patch(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        data = {"name": "NewcartName"}
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = cart.query.get(cart.id).to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 200
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_cart_item_patch_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        data = {"name": "NewcartName"}
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        # then
        assert response.status_code == 404


def test_cart_item_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()

        data_without = {"name": "NewTestcart"}
        data_std = {"name": "NewTestcart2"}
        data_staff = {"name": "NewTestcart3"}
        data_admin = {"name": "NewTestcart4"}

        api_route = f"{ROUTE}/{cart.id}"

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


def test_cart_item_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()

        data_name_to_short = {"name": "T" * 3}  # min 4
        data_name_to_long = {"name": "T" * 31}  # max 30
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response_name_to_short = client.patch(
            api_route, headers=admin_headers, json=data_name_to_short)
        response_name_to_long = client.patch(
            api_route, headers=admin_headers, json=data_name_to_long)

        response_name_to_short_data = json.loads(response_name_to_short.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_to_short.status_code == 400
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_to_short_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_to_short_data["message"]
        assert "name" in response_name_to_long_data["message"]


# TEST DELETE

#   CART

def test_cart_delete(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = cart.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_cart_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        create_cart_with_relations()
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = cart.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_cart_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart_without = create_cart_with_relations("Testcart")
        cart_std = create_cart_with_relations("Testcart2")
        cart_staff = create_cart_with_relations("Testcart3")
        cart_admin = create_cart_with_relations("Testcart4")

        api_route_without = f"{ROUTE}/{cart_without.id}"
        api_route_std = f"{ROUTE}/{cart_std.id}"
        api_route_staff = f"{ROUTE}/{cart_staff.id}"
        api_route_admin = f"{ROUTE}/{cart_admin.id}"

        # when
        response_without = client.delete(api_route_without)
        response_std = client.delete(api_route_std, headers=std_headers)
        response_staff = client.delete(api_route_staff, headers=staff_headers)
        response_admin = client.delete(api_route_admin, headers=admin_headers)

        result_data_db_without = cart.query.get(cart_without.id)
        result_data_db_std = cart.query.get(cart_std.id)
        result_data_db_staff = cart.query.get(cart_staff.id)
        result_data_db_admin = cart.query.get(cart_admin.id)

        # then
        assert response_without.status_code != 204
        assert response_std.status_code == 401
        assert response_staff.status_code == 204
        assert response_admin.status_code == 204

        assert result_data_db_without is not None
        assert result_data_db_std is not None
        assert result_data_db_staff is None
        assert result_data_db_admin is None


#   CART ITEM

def test_cart_item_delete(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = cart.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_cart_item_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        create_cart_with_relations()
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = cart.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_cart_item_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart_without = create_cart_with_relations("Testcart")
        cart_std = create_cart_with_relations("Testcart2")
        cart_staff = create_cart_with_relations("Testcart3")
        cart_admin = create_cart_with_relations("Testcart4")

        api_route_without = f"{ROUTE}/{cart_without.id}"
        api_route_std = f"{ROUTE}/{cart_std.id}"
        api_route_staff = f"{ROUTE}/{cart_staff.id}"
        api_route_admin = f"{ROUTE}/{cart_admin.id}"

        # when
        response_without = client.delete(api_route_without)
        response_std = client.delete(api_route_std, headers=std_headers)
        response_staff = client.delete(api_route_staff, headers=staff_headers)
        response_admin = client.delete(api_route_admin, headers=admin_headers)

        result_data_db_without = cart.query.get(cart_without.id)
        result_data_db_std = cart.query.get(cart_std.id)
        result_data_db_staff = cart.query.get(cart_staff.id)
        result_data_db_admin = cart.query.get(cart_admin.id)

        # then
        assert response_without.status_code != 204
        assert response_std.status_code == 401
        assert response_staff.status_code == 204
        assert response_admin.status_code == 204

        assert result_data_db_without is not None
        assert result_data_db_std is not None
        assert result_data_db_staff is None
        assert result_data_db_admin is None


#   SHARED USER

def test_cart_shared_user_delete(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart = create_cart_with_relations()
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = cart.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_cart_shared_user_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        create_cart_with_relations()
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = cart.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_cart_shared_user_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    assert False
    with app.app_context():
        # given
        cart_without = create_cart_with_relations("Testcart")
        cart_std = create_cart_with_relations("Testcart2")
        cart_staff = create_cart_with_relations("Testcart3")
        cart_admin = create_cart_with_relations("Testcart4")

        api_route_without = f"{ROUTE}/{cart_without.id}"
        api_route_std = f"{ROUTE}/{cart_std.id}"
        api_route_staff = f"{ROUTE}/{cart_staff.id}"
        api_route_admin = f"{ROUTE}/{cart_admin.id}"

        # when
        response_without = client.delete(api_route_without)
        response_std = client.delete(api_route_std, headers=std_headers)
        response_staff = client.delete(api_route_staff, headers=staff_headers)
        response_admin = client.delete(api_route_admin, headers=admin_headers)

        result_data_db_without = cart.query.get(cart_without.id)
        result_data_db_std = cart.query.get(cart_std.id)
        result_data_db_staff = cart.query.get(cart_staff.id)
        result_data_db_admin = cart.query.get(cart_admin.id)

        # then
        assert response_without.status_code != 204
        assert response_std.status_code == 401
        assert response_staff.status_code == 204
        assert response_admin.status_code == 204

        assert result_data_db_without is not None
        assert result_data_db_std is not None
        assert result_data_db_staff is None
        assert result_data_db_admin is None
"""
