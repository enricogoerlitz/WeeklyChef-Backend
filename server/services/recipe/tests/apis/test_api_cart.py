# flake8: noqa
import json

from flask import Flask, testing
from server.core.models.db_models.cart import Cart, CartItem, UserSharedEditCart
from server.core.models.db_models.user.user import User
from server.services.recipe.tests.apis.test_api_ingredient import (
    create_ingredient
)
from server.services.recipe.tests.apis.test_api_recipe import create_recipe
from server.services.recipe.tests.utils import create_obj


ROUTE = "/api/v1/cart"

# TEST GET


#   CART

"""
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


def test_cart_get_invalid_id(
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


def test_cart_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2

    with app.app_context():
        # given
        cart_user_2_not_shared = create_obj(
            Cart(
                name="CartName",
                owner_user_id=user_2.id,
                is_active=True
            )
        )
        cart_user_2_shared_with_user_1 = create_obj(
            Cart(
                name="CartName2",
                owner_user_id=user_2.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart_user_2_shared_with_user_1.id,
                user_id=user.id
            )
        )
        api_route_not_shared = f"{ROUTE}/{cart_user_2_not_shared.id}"
        api_route_shared = f"{ROUTE}/{cart_user_2_shared_with_user_1.id}"

        # when
        unauth_user = client.get(api_route_not_shared)
        user_2_cart_1_access = client.get(
            api_route_not_shared,
            headers=headers_2
        )
        user_2_cart_2_access = client.get(
            api_route_shared,
            headers=headers_2
        )
        user_1_cart_1_no_access = client.get(
            api_route_not_shared,
            headers=headers
        )
        user_1_cart_2_access = client.get(
            api_route_shared,
            headers=headers
        )

        user_2_cart_1_data = json.loads(user_2_cart_1_access.data)
        user_2_cart_2_data = json.loads(user_2_cart_2_access.data)
        user_1_cart_2_data = json.loads(user_1_cart_2_access.data)

        cart_1_expected_data = cart_user_2_not_shared.to_dict()
        cart_2_expected_data = cart_user_2_shared_with_user_1.to_dict()

        cart_1_expected_data["items"] = []
        cart_2_expected_data["items"] = []

        # then
        assert unauth_user.status_code != 200
        assert user_2_cart_1_access.status_code == 200
        assert user_2_cart_2_access.status_code == 200
        assert user_1_cart_1_no_access.status_code == 401
        assert user_1_cart_2_access.status_code == 200

        assert user_2_cart_1_data == cart_1_expected_data
        assert user_2_cart_2_data == cart_2_expected_data
        assert user_1_cart_2_data == cart_2_expected_data


def test_cart_get_clear(
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
        create_obj(
            CartItem(
                cart_id=cart.id,
                recipe_id=create_recipe(user.id).id,
                ingredient_id=create_ingredient().id,
                quantity=2,
                is_done=False
            )
        )
        api_route_get = f"{ROUTE}/{cart.id}"
        api_route_clear = f"{ROUTE}/{cart.id}/clear"

        # when
        response_with_data = client.get(api_route_get, headers=headers)
        response_clear = client.get(api_route_clear, headers=headers)
        response_cleared_data = client.get(api_route_get, headers=headers)

        result_data = json.loads(response_with_data.data)
        result_cleared_data = json.loads(response_cleared_data.data)

        # then
        assert response_with_data.status_code == 200
        assert response_clear.status_code == 204

        assert len(result_data["items"]) == 1
        assert len(result_cleared_data["items"]) == 0


def test_cart_get_clear_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1/clear"

        # when
        response = client.get(api_route, headers=admin_headers)

        # then
        assert response.status_code == 404


def test_cart_get_clear_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name="CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
            )
        )
        api_route_clear = f"{ROUTE}/{cart.id}/clear"
        
        # when
        response_owner = client.get(api_route_clear, headers=headers)
        response_access = client.get(api_route_clear, headers=headers_2)
        response_unauth = client.get(api_route_clear, headers=headers_3)

        # then
        assert response_unauth.status_code == 401
        assert response_owner.status_code == 204
        assert response_access.status_code == 204


# TEST GET-LIST

#   CART

def test_cart_get_list(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        COUNT = 3
        carts_user_1 = [
            create_obj(
                Cart(
                    name=f"CartName{i}",
                    owner_user_id=user.id,
                    is_active=True
                )
            )
                for i in range(0, COUNT)
        ]
        cart_user_2 = create_obj(
            Cart(
                name=f"CartName{COUNT + 1}",
                owner_user_id=user_2.id,
                is_active=True
            )
        )
        cart_user_3 = create_obj(
            Cart(
                name=f"CartName{COUNT + 2}",
                owner_user_id=user_3.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=carts_user_1[0].id,
                user_id=user_2.id
            )
        )
        api_route = f"{ROUTE}/"

        # when
        response = client.get(api_route, headers=headers)
        response_2 = client.get(api_route, headers=headers_2)
        response_3 = client.get(api_route, headers=headers_3)

        result_data_user_1 = json.loads(response.data)
        result_data_user_2 = json.loads(response_2.data)
        result_data_user_3 = json.loads(response_3.data)

        expected_data_user_1 = [cart.to_dict() for cart in carts_user_1]
        expected_data_user_2 = [carts_user_1[0], cart_user_2]
        expected_data_user_3 = [cart_user_3.to_dict()]
        
        expected_cart_data_1 = carts_user_1[0].to_dict()

        # then
        assert response.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 200

        assert len(result_data_user_1) == len(expected_data_user_1)
        assert len(result_data_user_2) == len(expected_data_user_2)
        assert len(result_data_user_3) == len(expected_data_user_3)

        assert result_data_user_1[0]["name"] == expected_cart_data_1["name"]
        assert result_data_user_1[0]["owner_user_id"] == expected_cart_data_1["owner_user_id"]
        assert result_data_user_1[0]["is_active"] == expected_cart_data_1["is_active"]
        assert "items" not in result_data_user_1[0]


def test_cart_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        api_route = f"{ROUTE}/"

        # when
        response_without = client.get(api_route)
        response_user = client.get(api_route, headers=headers)

        # then
        assert response_without.status_code != 200
        assert response_user.status_code == 200


# TEST-POST

def test_cart_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": "CartName",
            "is_active": True
        }
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Cart.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()
        expected_data["owner_user_id"] = user.id

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_cart_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": "CartName",
            "is_active": True
        }
        api_route = f"{ROUTE}/"

        # when
        response_without = client.post(
            api_route, json=data)
        response_user = client.post(
            api_route, headers=headers, json=data)

        # then
        assert response_without.status_code != 201
        assert response_user.status_code == 201


def test_cart_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data_name_is_null = {
            "is_active": True
        } # "name" not given
        data_is_active_is_null = {
            "name": "CartName",
        } # "is_active" not given
        data_name_to_short = {
            "name": "",
            "is_active": True
        } # "name" to short
        data_name_to_long = {
            "name": "T" * 51,
            "is_active": True
        } # "name" to long

        api_route = f"{ROUTE}/"

        # when
        response_name_is_null = client.post(
            api_route, headers=headers, json=data_name_is_null)
        response_is_active_is_null = client.post(
            api_route, headers=headers, json=data_is_active_is_null)
        response_name_to_short = client.post(
            api_route, headers=headers, json=data_name_to_short)
        response_name_to_long = client.post(
            api_route, headers=headers, json=data_name_to_long)

        response_name_is_null_data = json.loads(response_name_is_null.data)
        response_is_active_is_null_data = json.loads(response_is_active_is_null.data)
        response_name_to_short_data = json.loads(response_name_to_short.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_is_null.status_code == 400
        assert response_is_active_is_null.status_code == 400
        assert response_name_to_short.status_code == 400
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_is_null_data
        assert "message" in response_is_active_is_null_data
        assert "message" in response_name_to_short_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_is_null_data["message"]
        assert "is_active" in response_is_active_is_null_data["message"]
        assert "name" in response_name_to_short_data["message"]
        assert "name" in response_name_to_long_data["message"]


#   CART ITEM

def test_cart_item_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        ingredient = create_ingredient()
        data = {
            "recipe_id": recipe.id,
            "ingredient_id": ingredient.id,
            "quantity": 2,
            "is_done": True,
        }
        api_route = f"{ROUTE}/{cart.id}/item"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = CartItem.query.filter_by(**data).first().to_dict()

        expected_data = data.copy()
        expected_data["cart_id"] = cart.id
        expected_data["ingredient"] = ingredient.to_dict()
        expected_data["recipe"] = ingredient.to_dict()

        # then
        assert response.status_code == 201

        assert result_data["id"] == result_data_db["id"]
        assert result_data["is_done"] == result_data_db["is_done"]
        assert result_data["quantity"] == result_data_db["quantity"]
        assert result_data["recipe"]["id"] == result_data_db["recipe_id"]
        assert result_data["ingredient"]["id"] == result_data_db["ingredient_id"]


def test_cart_item_post_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        api_route = f"{ROUTE}/1/item"

        # when
        response = client.post(api_route, headers=headers, json={})
        response_data = json.loads(response.data)

        # then
        assert response.status_code == 404

        assert "message" in response_data


def test_cart_item_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        ingredient = create_ingredient()
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
            )
        )
        data = {
            "recipe_id": recipe.id,
            "ingredient_id": ingredient.id,
            "quantity": 2,
            "is_done": True,
        }
        api_route = f"{ROUTE}/{cart.id}/item"

        # when
        response_without = client.post(
            api_route, json=data)
        response_user_owner = client.post(
            api_route, headers=headers, json=data)
        response_user_shared_with = client.post(
            api_route, headers=headers_2, json=data)
        response_user_access_denied= client.post(
            api_route, headers=headers_3, json=data)

        # then
        assert response_without.status_code != 201
        assert response_user_owner.status_code == 201
        assert response_user_shared_with.status_code == 201
        assert response_user_access_denied.status_code == 401


def test_cart_item_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        ingredient = create_ingredient()
        data_recipe_id_not_exisiting = {
            "recipe_id": -1,
            "ingredient_id": ingredient.id,
            "quantity": 1,
            "is_done": True
        }
        data_ingredient_id_is_null = {
            "quantity": 1,
            "is_done": True
        }
        data_quantity_is_null = {
            "ingredient_id": ingredient.id,
            "is_done": True
        }
        data_quantity_to_small = {
            "ingredient_id": ingredient.id,
            "quantity": -1,
            "is_done": True
        }
        data_is_done_is_null = {
            "ingredient_id": ingredient.id,
            "quantity": 1
        }
        
        api_route = f"{ROUTE}/{cart.id}/item"

        # when
        resp_recipe_id_not_exisiting = client.post(
            api_route, headers=headers, json=data_recipe_id_not_exisiting)
        resp_ingredient_id_is_null = client.post(
            api_route, headers=headers, json=data_ingredient_id_is_null)
        resp_quantity_is_null = client.post(
            api_route, headers=headers, json=data_quantity_is_null)
        resp_quantity_to_small = client.post(
            api_route, headers=headers, json=data_quantity_to_small)
        resp_is_done_is_null = client.post(
            api_route, headers=headers, json=data_is_done_is_null)

        resp_recipe_id_not_exisiting_data = json.loads(resp_recipe_id_not_exisiting.data)
        resp_ingredient_id_is_null_data = json.loads(resp_ingredient_id_is_null.data)
        resp_quantity_is_null_data = json.loads(resp_quantity_is_null.data)
        resp_quantity_to_small_data = json.loads(resp_quantity_to_small.data)
        resp_is_done_is_null_data = json.loads(resp_is_done_is_null.data)

        # then
        assert resp_recipe_id_not_exisiting.status_code == 404
        assert resp_ingredient_id_is_null.status_code == 400
        assert resp_quantity_is_null.status_code == 400
        assert resp_quantity_to_small.status_code == 400
        assert resp_is_done_is_null.status_code == 400

        assert "message" in resp_recipe_id_not_exisiting_data
        assert "message" in resp_ingredient_id_is_null_data
        assert "message" in resp_quantity_is_null_data
        assert "message" in resp_quantity_to_small_data
        assert "message" in resp_is_done_is_null_data

        assert "recipe_id" in resp_recipe_id_not_exisiting_data["message"]
        assert "ingredient_id" in resp_ingredient_id_is_null_data["message"]
        assert "quantity" in resp_quantity_is_null_data["message"]
        assert "quantity" in resp_quantity_to_small_data["message"]
        assert "is_done" in resp_is_done_is_null_data["message"]


#   SHARED USER

def test_cart_shared_user_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data = {
            "cart_id": cart.id,
            "user_id": user.id
        }
        api_route = f"{ROUTE}/{cart.id}/access/edit/user/{user.id}"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = UserSharedEditCart.query.get((cart.id, user.id)).to_dict()

        # then
        assert response.status_code == 201
        assert result_data_db == result_data


def test_cart_shared_user_post_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1/access/edit/user/{user.id}"

        # when
        response = client.post(api_route, headers=headers, json={})

        # then
        assert response.status_code == 404


def test_cart_shared_user_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        api_route = f"{ROUTE}/{cart.id}/access/edit/user/{user_2.id}"

        # when
        response_without = client.post(
            api_route, json={})
        response_user_owner = client.post(
            api_route, headers=headers, json={})
        response_user_2_shared_but_access_denied = client.post(
            api_route, headers=headers_2, json={})
        response_user_3 = client.post(
            api_route, headers=headers_3, json={})

        # then
        assert response_without.status_code != 201
        assert response_user_owner.status_code == 201
        assert response_user_2_shared_but_access_denied.status_code == 401
        assert response_user_3.status_code == 401


def test_cart_shared_user_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        api_route = f"{ROUTE}/{cart.id}/access/edit/user/-1"

        # when
        response = client.post(api_route, headers=headers, json={})

        # then
        assert response.status_code == 404


# TEST UPDATE

#   CART

def test_cart_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data = {
            "name": "CartUpdatedName",
            "is_active": False
        }
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = cart.query.get(cart.id).to_dict()

        # then
        assert response.status_code == 200
        assert result_data_db == result_data


def test_cart_patch_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=admin_headers, json={})

        # then
        assert response.status_code == 404


def test_cart_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
            )
        )

        data_without = {"name": "NewTestcart"}
        data_user_owner = {"name": "NewTestcart2"}
        data_user_2_can_edit = {"name": "NewTestcart3"}
        data_user_3_access_denied = {"name": "NewTestcart4"}

        api_route = f"{ROUTE}/{cart.id}"

        # when
        response_without = client.patch(
            api_route, json=data_without)
        response_owner = client.patch(
            api_route, headers=headers, json=data_user_owner)
        response_can_edit = client.patch(
            api_route, headers=headers_2, json=data_user_2_can_edit)
        response_access_denied = client.patch(
            api_route, headers=headers_3, json=data_user_3_access_denied)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 200
        assert response_can_edit.status_code == 200
        assert response_access_denied.status_code == 401


def test_cart_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data_name_to_short = {"name": ""}
        data_name_to_long = {"name": "T" * 51}
        data_is_active_is_null = {"is_active": None}
        data_is_owner_user_id_is_readonly = {"owner_user_id": 1}

        api_route = f"{ROUTE}/{cart.id}"

        # when
        resp_name_to_short = client.patch(api_route, headers=headers, json=data_name_to_short)
        resp_name_to_long = client.patch(api_route, headers=headers, json=data_name_to_long)
        resp_is_active_is_null = client.patch(api_route, headers=headers, json=data_is_active_is_null)
        resp_is_owner_user_id_is_readonly = client.patch(api_route, headers=headers, json=data_is_owner_user_id_is_readonly)

        resp_name_to_short_data = json.loads(resp_name_to_short.data)
        resp_name_to_long_data = json.loads(resp_name_to_long.data)
        resp_is_active_is_null_data = json.loads(resp_is_active_is_null.data)
        resp_is_owner_user_id_is_readonly_data = json.loads(resp_is_owner_user_id_is_readonly.data)

        # then
        assert resp_name_to_short.status_code == 400
        assert resp_name_to_long.status_code == 400
        assert resp_is_active_is_null.status_code == 400
        assert resp_is_owner_user_id_is_readonly.status_code == 400

        assert "message" in resp_name_to_short_data
        assert "message" in resp_name_to_long_data
        assert "message" in resp_is_active_is_null_data
        assert "message" in resp_is_owner_user_id_is_readonly_data

        assert "name" in resp_name_to_short_data["message"]
        assert "name" in resp_name_to_long_data["message"]
        assert "is_active" in resp_is_active_is_null_data["message"]
        assert "owner_user_id" in resp_is_owner_user_id_is_readonly_data["message"]
        assert "read only" in resp_is_owner_user_id_is_readonly_data["message"]


#   CART ITEM

def test_cart_item_patch(
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
        data = {
            "quantity": 4,
            "is_done": False
        }
        api_route = f"{ROUTE}/{cart.id}/item/{cart_item.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = CartItem.query.get(cart_item.id).to_dict()

        # then
        print(result_data)
        assert response.status_code == 200
        assert result_data["quantity"] == data["quantity"]
        assert result_data["is_done"] == data["is_done"]


def test_cart_item_patch_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=admin_headers, json={})

        # then
        assert response.status_code == 404


def test_cart_item_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
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

        data_without = {"quantity": 5}
        data_user_owner = {"quantity": 5}
        data_user_2_can_edit = {"quantity": 5}
        data_user_3_access_denied = {"quantity": 5}

        api_route = f"{ROUTE}/{cart.id}/item/{cart_item.id}"

        # when
        response_without = client.patch(
            api_route, json=data_without)
        response_owner = client.patch(
            api_route, headers=headers, json=data_user_owner)
        response_can_edit = client.patch(
            api_route, headers=headers_2, json=data_user_2_can_edit)
        response_access_denied = client.patch(
            api_route, headers=headers_3, json=data_user_3_access_denied)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 200
        assert response_can_edit.status_code == 200
        assert response_access_denied.status_code == 401


def test_cart_item_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
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
        data_quantity_to_low = {"quantity": -1}
        data_is_done_is_null = {"is_done": None}
        api_route = f"{ROUTE}/{cart.id}/item/{cart_item.id}"

        # when
        response_quantity_to_low = client.patch(
            api_route, headers=headers, json=data_quantity_to_low)
        response_is_done_is_null = client.patch(
            api_route, headers=headers, json=data_is_done_is_null)

        response_quantity_to_low_data = json.loads(response_quantity_to_low.data)
        response_is_done_is_null_data = json.loads(response_is_done_is_null.data)

        # then
        assert response_quantity_to_low.status_code == 400
        assert response_is_done_is_null.status_code == 400

        assert "message" in response_quantity_to_low_data
        assert "message" in response_is_done_is_null_data

        assert "quantity" in response_quantity_to_low_data["message"]
        assert "is_done" in response_is_done_is_null_data["message"]


# TEST DELETE

#   CART

def test_cart_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/{cart.id}"

        # when
        response = client.delete(api_route, headers=headers)

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
    with app.app_context():
        # given
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=admin_headers)

        # then
        assert response.status_code == 404


def test_cart_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        cart_2 = create_obj(
            Cart(
                name=f"CartName2",
                owner_user_id=user.id,
                is_active=True
            )
        )

        api_route = f"{ROUTE}/{cart.id}"
        api_route_2 = f"{ROUTE}/{cart_2.id}"

        # when
        response_without = client.delete(
            api_route_2)
        response_owner = client.delete(
            api_route, headers=headers)
        response_can_edit = client.delete(
            api_route_2, headers=headers_2)
        response_access_denied = client.delete(
            api_route_2, headers=headers_3)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 204
        assert response_can_edit.status_code == 401
        assert response_access_denied.status_code == 401


#   CART ITEM

def test_cart_item_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
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
        db_model_count_before = CartItem.query.count()
        api_route = f"{ROUTE}/{cart.id}/item/{cart_item.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = CartItem.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_cart_item_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        db_model_count_before = cart.query.count()
        api_route = f"{ROUTE}/{cart.id}/item/-1"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = cart.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_cart_item_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
            )
        )
        recipe = create_recipe(user.id)
        ingredient = create_ingredient()
        cart_item = create_obj(
            CartItem(
                cart_id=cart.id,
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=2,
                is_done=False
            )
        )
        cart_item_2 = create_obj(
            CartItem(
                cart_id=cart.id,
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=2,
                is_done=False
            )
        )
        cart_item_3 = create_obj(
            CartItem(
                cart_id=cart.id,
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=2,
                is_done=False
            )
        )

        api_route_item_1 = f"{ROUTE}/{cart.id}/item/{cart_item.id}"
        api_route_item_2 = f"{ROUTE}/{cart.id}/item/{cart_item_2.id}"
        api_route_item_3 = f"{ROUTE}/{cart.id}/item/{cart_item_3.id}"

        # when
        response_without = client.delete(api_route_item_1)
        response_owner = client.delete(api_route_item_1, headers=headers)
        response_can_edit = client.delete(api_route_item_2, headers=headers_2)
        response_access_denied = client.delete(api_route_item_3, headers=headers_3)

        # then
        assert response_without.status_code != 204
        assert response_owner.status_code == 204
        assert response_can_edit.status_code == 204
        assert response_access_denied.status_code == 401


#   SHARED USER

def test_cart_shared_user_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
            )
        )
        db_model_count_before = UserSharedEditCart.query.count()
        api_route = f"{ROUTE}/{cart.id}/access/edit/user/{user_2.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = UserSharedEditCart.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_cart_shared_user_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
            )
        )
        db_model_count_before = cart.query.count()
        api_route_invalid_cart_id = f"{ROUTE}/-1/access/edit/user/{user_2.id}"
        api_route_invalid_user_id = f"{ROUTE}/{cart.id}/access/edit/user/-1"

        # when
        response_invalid_cart_id = client.delete(api_route_invalid_cart_id, headers=headers)
        response_invalid_user_id = client.delete(api_route_invalid_user_id, headers=headers)

        db_model_count_after = cart.query.count()

        # then
        assert response_invalid_cart_id.status_code == 404
        assert response_invalid_user_id.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_cart_shared_user_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        cart = create_obj(
            Cart(
                name=f"CartName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_2.id
            )
        )
        create_obj(
            UserSharedEditCart(
                cart_id=cart.id,
                user_id=user_3.id
            )
        )

        api_route = f"{ROUTE}/{cart.id}/access/edit/user/{user_2.id}"
        api_route_2 = f"{ROUTE}/{cart.id}/access/edit/user/{user_3.id}"

        # when
        response_without = client.delete(api_route)
        response_owner = client.delete(api_route, headers=headers)
        response_can_edit = client.delete(api_route_2, headers=headers_2)
        response_access_denied = client.delete(api_route_2, headers=headers_3)

        # then
        assert response_without.status_code != 204
        assert response_owner.status_code == 204
        assert response_can_edit.status_code == 401
        assert response_access_denied.status_code == 401
"""