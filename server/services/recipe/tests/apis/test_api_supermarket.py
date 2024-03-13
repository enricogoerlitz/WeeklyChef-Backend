# flake8: noqa
import json

from flask import Flask, testing
from server.core.models.db_models.supermarket import (
    Supermarket, SupermarketArea, UserSharedEditSupermarket
)
from server.core.models.db_models.user.user import User
from server.services.recipe.tests.apis.test_api_ingredient import (
    create_ingredient
)
from server.services.recipe.tests.apis.test_api_recipe import create_recipe
from server.services.recipe.tests.utils import create_obj


ROUTE = "/api/v1/supermarket"

# TEST GET


#   SUPERMARKET


def test_supermarket_get(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name="SupermarketName",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        area = create_obj(
            SupermarketArea(
                name="Area1",
                order_number=1,
                supermarket_id=supermarket.id
            )
        )
        api_route = f"{ROUTE}/{supermarket.id}"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = supermarket.to_dict()
        expected_data["areas"] = [area.to_dict()]

        # then
        assert response.status_code == 200

        assert result_data == expected_data


def test_supermarket_get_invalid_id(
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


def test_supermarket_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2

    with app.app_context():
        # given
        supermarket_user_2_not_shared = create_obj(
            Supermarket(
                name="SupermarketName",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        supermarket_user_2_shared_with_user_1 = create_obj(
            Supermarket(
                name="SupermarketName2",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket_user_2_shared_with_user_1.id,
                user_id=user.id
            )
        )
        api_route_not_shared = f"{ROUTE}/{supermarket_user_2_not_shared.id}"
        api_route_shared = f"{ROUTE}/{supermarket_user_2_shared_with_user_1.id}"

        # when
        unauth_user = client.get(api_route_not_shared)
        user_2_supermarket_1_access = client.get(
            api_route_not_shared,
            headers=headers_2
        )
        user_2_supermarket_2_access = client.get(
            api_route_shared,
            headers=headers_2
        )
        user_1_supermarket_1_no_access = client.get(
            api_route_not_shared,
            headers=headers
        )
        user_1_supermarket_2_access = client.get(
            api_route_shared,
            headers=headers
        )

        # then
        assert unauth_user.status_code != 200
        assert user_2_supermarket_1_access.status_code == 200
        assert user_2_supermarket_2_access.status_code == 200
        assert user_1_supermarket_1_no_access.status_code == 200
        assert user_1_supermarket_2_access.status_code == 200


# TEST GET-LIST

#   SUPERMARKET

def test_supermarket_get_list(
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
        supermarkets_user_1 = [
            create_obj(
                Supermarket(
                    name=f"SupermarketName{i}",
                    street="Street",
                    postcode="182923",
                    district="Berlin",
                    owner_user_id=user.id
                )
            )
                for i in range(0, COUNT)
        ]
        supermarket_user_2 = create_obj(
            Supermarket(
                name="SupermarketName",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        supermarket_user_3 = create_obj(
            Supermarket(
                name=f"SupermarketName{COUNT + 2}",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarkets_user_1[0].id,
                user_id=user_2.id
            )
        )
        api_route = f"{ROUTE}/"

        # when
        response_without = client.get(api_route)
        response = client.get(api_route, headers=headers)
        response_2 = client.get(api_route, headers=headers_2)
        response_3 = client.get(api_route, headers=headers_3)

        result_data_user_1 = json.loads(response.data)
        result_data_user_2 = json.loads(response_2.data)
        result_data_user_3 = json.loads(response_3.data)

        # then
        assert response_without.status_code != 200
        assert response.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 200

        assert len(result_data_user_1) == COUNT + 2
        assert len(result_data_user_2) == COUNT + 2
        assert len(result_data_user_3) == COUNT + 2


def test_supermarket_get_list_query_params(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    # TODO: Implement Query 
    assert False


def test_supermarket_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        create_obj(
            Supermarket(
                name=f"SupermarketName",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
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

def test_supermarket_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": f"SupermarketName",
            "street": "Street",
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Supermarket.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()
        expected_data["owner_user_id"] = user.id

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_supermarket_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": f"SupermarketName",
            "street": "Street",
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
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


def test_supermarket_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        create_obj(
            Supermarket(
                name=f"SupermarketName-Dup",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        data_duplicate = {
            "name": "SupermarketName-Dup",
            "street": "Street",
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_name_is_null = {
            "street": "Street",
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_name_to_short = {
            "name": "T" * 2,
            "street": "Street",
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_name_to_long = {
            "name": "T" * 26,
            "street": "Street",
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_street_is_null = {
            "name": "SupermarketName",
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_street_to_short = {
            "name": "SupermarketName",
            "street": "T" * 2,
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_street_to_long = {
            "name": "SupermarketName",
            "street": "T" * 101,
            "postcode": "182923",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_postcode_is_null = {
            "name": "SupermarketName",
            "street": "Street",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_postcode_to_short = {
            "name": "SupermarketName",
            "street": "Street",
            "postcode": "",
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_postcode_to_long = {
            "name": "SupermarketName",
            "street": "Street",
            "postcode": "T" * 26,
            "district": "Berlin",
            "owner_user_id": user.id
        }
        data_district_is_null = {
            "name": "SupermarketName",
            "street": "Street",
            "postcode": "182923",
            "owner_user_id": user.id
        }
        data_district_to_short = {
            "name": "SupermarketName",
            "street": "Street",
            "postcode": "182923",
            "district": "",
            "owner_user_id": user.id
        }
        data_district_to_long = {
            "name": "SupermarketName",
            "street": "Street",
            "postcode": "182923",
            "district": "T" * 51,
            "owner_user_id": user.id
        }

        api_route = f"{ROUTE}/"

        # when
        resp_duplicate = client.post(api_route, headers=headers, json=data_duplicate)
        resp_name_is_null = client.post(api_route, headers=headers, json=data_name_is_null)
        resp_name_to_short = client.post(api_route, headers=headers, json=data_name_to_short)
        resp_name_to_long = client.post(api_route, headers=headers, json=data_name_to_long)
        resp_street_is_null = client.post(api_route, headers=headers, json=data_street_is_null)
        resp_street_to_short = client.post(api_route, headers=headers, json=data_street_to_short)
        resp_street_to_long = client.post(api_route, headers=headers, json=data_street_to_long)
        resp_postcode_is_null = client.post(api_route, headers=headers, json=data_postcode_is_null)
        resp_postcode_to_short = client.post(api_route, headers=headers, json=data_postcode_to_short)
        resp_postcode_to_long = client.post(api_route, headers=headers, json=data_postcode_to_long)
        resp_district_is_null = client.post(api_route, headers=headers, json=data_district_is_null)
        resp_district_to_short = client.post(api_route, headers=headers, json=data_district_to_short)
        resp_district_to_long = client.post(api_route, headers=headers, json=data_district_to_long)

        resp_duplicate_data = json.loads(resp_duplicate.data)
        resp_name_is_null_data = json.loads(resp_name_is_null.data)
        resp_name_to_short_data = json.loads(resp_name_to_short.data)
        resp_name_to_long_data = json.loads(resp_name_to_long.data)
        resp_street_is_null_data = json.loads(resp_street_is_null.data)
        resp_street_to_short_data = json.loads(resp_street_to_short.data)
        resp_street_to_long_data = json.loads(resp_street_to_long.data)
        resp_postcode_is_null_data = json.loads(resp_postcode_is_null.data)
        resp_postcode_to_short_data = json.loads(resp_postcode_to_short.data)
        resp_postcode_to_long_data = json.loads(resp_postcode_to_long.data)
        resp_district_is_null_data = json.loads(resp_district_is_null.data)
        resp_district_to_short_data = json.loads(resp_district_to_short.data)
        resp_district_to_long_data = json.loads(resp_district_to_long.data)

        # then
        assert resp_duplicate.status_code == 409
        assert resp_name_is_null.status_code == 400
        assert resp_name_to_short.status_code == 400
        assert resp_name_to_long.status_code == 400
        assert resp_street_is_null.status_code == 400
        assert resp_street_to_short.status_code == 400
        assert resp_street_to_long.status_code == 400
        assert resp_postcode_is_null.status_code == 400
        assert resp_postcode_to_short.status_code == 400
        assert resp_postcode_to_long.status_code == 400
        assert resp_district_is_null.status_code == 400
        assert resp_district_to_short.status_code == 400
        assert resp_district_to_long.status_code == 400

        assert "message" in resp_duplicate_data
        assert "message" in resp_name_is_null_data
        assert "message" in resp_name_to_short_data
        assert "message" in resp_name_to_long_data
        assert "message" in resp_street_is_null_data
        assert "message" in resp_street_to_short_data
        assert "message" in resp_street_to_long_data
        assert "message" in resp_postcode_is_null_data
        assert "message" in resp_postcode_to_short_data
        assert "message" in resp_postcode_to_long_data
        assert "message" in resp_district_is_null_data
        assert "message" in resp_district_to_short_data
        assert "message" in resp_district_to_long_data

        assert "already existing" in resp_duplicate_data["message"]
        assert "name" in resp_name_is_null_data["message"]
        assert "name" in resp_name_to_short_data["message"]
        assert "name" in resp_name_to_long_data["message"]
        assert "street" in resp_street_is_null_data["message"]
        assert "street" in resp_street_to_short_data["message"]
        assert "street" in resp_street_to_long_data["message"]
        assert "postcode" in resp_postcode_is_null_data["message"]
        assert "postcode" in resp_postcode_to_short_data["message"]
        assert "postcode" in resp_postcode_to_long_data["message"]
        assert "district" in resp_district_is_null_data["message"]
        assert "district" in resp_district_to_short_data["message"]
        assert "district" in resp_district_to_long_data["message"]


#   SUPERMARKET AREA

def test_supermarket_area_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        data = {
            "name": "AreaName",
            "order_number": 1,
            "supermarket_id": supermarket.id
        }
        api_route = f"{ROUTE}/{supermarket.id}/area"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = SupermarketArea.query.filter_by(**data).first().to_dict()

        # then
        assert response.status_code == 201

        assert result_data == result_data_db


def test_supermarket_area_post_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        api_route = f"{ROUTE}/1/area"

        # when
        response = client.post(api_route, headers=headers, json={})
        response_data = json.loads(response.data)

        # then
        assert response.status_code == 404

        assert "message" in response_data


def test_supermarket_area_post_authorization(
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
        supermarket = create_obj(
            Supermarket(
                name="SupermarketName",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_2.id
            )
        )
        data = {
            "name": "AreaName2",
            "order_number": 2,
            "supermarket_id": supermarket.id
        }
        data_2 = {
            "name": "AreaName3",
            "order_number": 3,
            "supermarket_id": supermarket.id
        }
        api_route = f"{ROUTE}/{supermarket.id}/area"

        # when
        response_without = client.post(
            api_route, json=data)
        response_user_owner = client.post(
            api_route, headers=headers, json=data)
        response_user_shared_with = client.post(
            api_route, headers=headers_2, json=data_2)
        response_user_access_denied= client.post(
            api_route, headers=headers_3, json=data)

        # then
        assert response_without.status_code != 201
        assert response_user_owner.status_code == 201
        assert response_user_shared_with.status_code == 201
        assert response_user_access_denied.status_code == 401


def test_supermarket_area_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name="SupermarketName",
                street="Street",
                postcode="182923",
                district="Berlin",
                owner_user_id=user.id
            )
        )
        data_name_is_null = {
            "order_number": 1
        }
        data_name_is_to_short = {
            "name": "T" * 2,
            "order_number": 1
        }
        data_name_is_to_long = {
            "name": "T" * 26,
            "order_number": 1
        }
        data_order_number_is_null = {
            "name": "SupermarketArea"
        }
        data_order_number_to_low = {
            "name": "SupermarketArea",
            "order_number": 0
        }
        
        api_route = f"{ROUTE}/{supermarket.id}/area"

        # when
        resp_name_is_null = client.post(api_route, headers=headers, json=data_name_is_null)
        resp_name_is_to_short = client.post(api_route, headers=headers, json=data_name_is_to_short)
        resp_name_is_to_long = client.post(api_route, headers=headers, json=data_name_is_to_long)
        resp_order_number_is_null = client.post(api_route, headers=headers, json=data_order_number_is_null)
        resp_order_number_to_low = client.post(api_route, headers=headers, json=data_order_number_to_low)

        resp_name_is_null_data = json.loads(resp_name_is_null.data)
        resp_name_is_to_short_data = json.loads(resp_name_is_to_short.data)
        resp_name_is_to_long_data = json.loads(resp_name_is_to_long.data)
        resp_order_number_is_null_data = json.loads(resp_order_number_is_null.data)
        resp_order_number_to_low_data = json.loads(resp_order_number_to_low.data)

        # then
        assert resp_name_is_null.status_code == 400
        assert resp_name_is_to_short.status_code == 400
        assert resp_name_is_to_long.status_code == 400
        assert resp_order_number_is_null.status_code == 400
        assert resp_order_number_to_low.status_code == 400

        assert "message" in resp_name_is_null_data
        assert "message" in resp_name_is_to_short_data
        assert "message" in resp_name_is_to_long_data
        assert "message" in resp_order_number_is_null_data
        assert "message" in resp_order_number_to_low_data

        assert "name" in resp_name_is_null_data["message"]
        assert "name" in resp_name_is_to_short_data["message"]
        assert "name" in resp_name_is_to_long_data["message"]
        assert "order_number" in resp_order_number_is_null_data["message"]
        assert "order_number" in resp_order_number_to_low_data["message"]

        
#   SUPERMARKET AREA INGREDIENT

# post_supermarket_area_ingredient
# post_supermarket_area_ingredient_auth

#   SHARED USER
"""
def test_supermarket_shared_user_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data = {
            "supermarket_id": supermarket.id,
            "user_id": user.id
        }
        api_route = f"{ROUTE}/{supermarket.id}/access/edit/user/{user.id}"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = UserSharedEditSupermarket.query.get((supermarket.id, user.id)).to_dict()

        # then
        assert response.status_code == 201
        assert result_data_db == result_data


def test_supermarket_shared_user_post_invalid_id(
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


def test_supermarket_shared_user_post_authorization(
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
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        api_route = f"{ROUTE}/{supermarket.id}/access/edit/user/{user_2.id}"

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


def test_supermarket_shared_user_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        api_route = f"{ROUTE}/{supermarket.id}/access/edit/user/-1"

        # when
        response = client.post(api_route, headers=headers, json={})

        # then
        assert response.status_code == 404


# TEST UPDATE

#   SUPERMARKET

def test_supermarket_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data = {
            "name": "SupermarketUpdatedName",
            "is_active": False
        }
        api_route = f"{ROUTE}/{supermarket.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = supermarket.query.get(supermarket.id).to_dict()

        # then
        assert response.status_code == 200
        assert result_data_db == result_data


def test_supermarket_patch_invalid_id(
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


def test_supermarket_patch_authorization(
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
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_2.id
            )
        )

        data_without = {"name": "NewTestsupermarket"}
        data_user_owner = {"name": "NewTestsupermarket2"}
        data_user_2_can_edit = {"name": "NewTestsupermarket3"}
        data_user_3_access_denied = {"name": "NewTestsupermarket4"}

        api_route = f"{ROUTE}/{supermarket.id}"

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


def test_supermarket_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data_name_to_short = {"name": ""}
        data_name_to_long = {"name": "T" * 51}
        data_is_active_is_null = {"is_active": None}
        data_is_owner_user_id_is_readonly = {"owner_user_id": 1}

        api_route = f"{ROUTE}/{supermarket.id}"

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


#   SUPERMARKET AREA

def test_supermarket_area_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name="SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        supermarket_area = create_obj(
            SupermarketArea(
                supermarket_id=supermarket.id,
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
        api_route = f"{ROUTE}/{supermarket.id}/area/{supermarket_area.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = SupermarketArea.query.get(supermarket_area.id).to_dict()

        # then
        print(result_data)
        assert response.status_code == 200
        assert result_data["quantity"] == data["quantity"]
        assert result_data["is_done"] == data["is_done"]


def test_supermarket_area_patch_invalid_id(
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


def test_supermarket_area_patch_authorization(
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
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_2.id
            )
        )
        supermarket_area = create_obj(
            SupermarketArea(
                supermarket_id=supermarket.id,
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

        api_route = f"{ROUTE}/{supermarket.id}/area/{supermarket_area.id}"

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


def test_supermarket_area_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        supermarket_area = create_obj(
            SupermarketArea(
                supermarket_id=supermarket.id,
                recipe_id=create_recipe(user.id).id,
                ingredient_id=create_ingredient().id,
                quantity=2,
                is_done=False
            )
        )
        data_quantity_to_low = {"quantity": -1}
        data_is_done_is_null = {"is_done": None}
        api_route = f"{ROUTE}/{supermarket.id}/area/{supermarket_area.id}"

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


# patch_supermarket_area_reorder        


#   SUPERMARKET AREA INGREDIENT

# patch_supermarket_area_ingredient
# patch_supermarket_area_ingredient_auth


# TEST DELETE

#   SUPERMARKET

def test_supermarket_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        db_model_count_before = supermarket.query.count()
        api_route = f"{ROUTE}/{supermarket.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = supermarket.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_supermarket_delete_invalid_id(
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


def test_supermarket_delete_authorization(
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
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        supermarket_2 = create_obj(
            Supermarket(
                name=f"SupermarketName2",
                owner_user_id=user.id,
                is_active=True
            )
        )

        api_route = f"{ROUTE}/{supermarket.id}"
        api_route_2 = f"{ROUTE}/{supermarket_2.id}"

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


#   SUPERMARKET ITEM

def test_supermarket_area_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        supermarket_area = create_obj(
            SupermarketArea(
                supermarket_id=supermarket.id,
                recipe_id=create_recipe(user.id).id,
                ingredient_id=create_ingredient().id,
                quantity=2,
                is_done=False
            )
        )
        db_model_count_before = SupermarketArea.query.count()
        api_route = f"{ROUTE}/{supermarket.id}/area/{supermarket_area.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = SupermarketArea.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_supermarket_area_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        db_model_count_before = supermarket.query.count()
        api_route = f"{ROUTE}/{supermarket.id}/area/-1"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = supermarket.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_supermarket_area_delete_authorization(
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
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_2.id
            )
        )
        recipe = create_recipe(user.id)
        ingredient = create_ingredient()
        supermarket_area = create_obj(
            SupermarketArea(
                supermarket_id=supermarket.id,
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=2,
                is_done=False
            )
        )
        supermarket_area_2 = create_obj(
            SupermarketArea(
                supermarket_id=supermarket.id,
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=2,
                is_done=False
            )
        )
        supermarket_area_3 = create_obj(
            SupermarketArea(
                supermarket_id=supermarket.id,
                recipe_id=recipe.id,
                ingredient_id=ingredient.id,
                quantity=2,
                is_done=False
            )
        )

        api_route_area_1 = f"{ROUTE}/{supermarket.id}/area/{supermarket_area.id}"
        api_route_area_2 = f"{ROUTE}/{supermarket.id}/area/{supermarket_area_2.id}"
        api_route_area_3 = f"{ROUTE}/{supermarket.id}/area/{supermarket_area_3.id}"

        # when
        response_without = client.delete(api_route_area_1)
        response_owner = client.delete(api_route_area_1, headers=headers)
        response_can_edit = client.delete(api_route_area_2, headers=headers_2)
        response_access_denied = client.delete(api_route_area_3, headers=headers_3)

        # then
        assert response_without.status_code != 204
        assert response_owner.status_code == 204
        assert response_can_edit.status_code == 204
        assert response_access_denied.status_code == 401


#   SUPERMARKET AREA INGREDIENT

# delete_supermarket_area_ingredient
# delete_supermarket_area_ingredient_auth


#   SHARED USER

def test_supermarket_shared_user_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_2.id
            )
        )
        db_model_count_before = UserSharedEditSupermarket.query.count()
        api_route = f"{ROUTE}/{supermarket.id}/access/edit/user/{user_2.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = UserSharedEditSupermarket.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_supermarket_shared_user_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_2.id
            )
        )
        db_model_count_before = supermarket.query.count()
        api_route_invalid_supermarket_id = f"{ROUTE}/-1/access/edit/user/{user_2.id}"
        api_route_invalid_user_id = f"{ROUTE}/{supermarket.id}/access/edit/user/-1"

        # when
        response_invalid_supermarket_id = client.delete(api_route_invalid_supermarket_id, headers=headers)
        response_invalid_user_id = client.delete(api_route_invalid_user_id, headers=headers)

        db_model_count_after = supermarket.query.count()

        # then
        assert response_invalid_supermarket_id.status_code == 404
        assert response_invalid_user_id.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_supermarket_shared_user_delete_authorization(
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
        supermarket = create_obj(
            Supermarket(
                name=f"SupermarketName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_2.id
            )
        )
        create_obj(
            UserSharedEditSupermarket(
                supermarket_id=supermarket.id,
                user_id=user_3.id
            )
        )

        api_route = f"{ROUTE}/{supermarket.id}/access/edit/user/{user_2.id}"
        api_route_2 = f"{ROUTE}/{supermarket.id}/access/edit/user/{user_3.id}"

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