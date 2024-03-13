# flake8: noqa
import json

from datetime import timedelta, datetime
from flask import Flask, testing
import server.core.models.db_models
from server.core.models.db_models.planner import (
    RecipePlanner, RecipePlannerItem, UserSharedRecipePlanner
)
from server.core.models.db_models.user.user import User
from server.services.recipe.tests.apis.test_api_ingredient import (
    create_ingredient
)
from server.services.recipe.tests.apis.test_api_recipe import create_recipe
from server.services.recipe.tests.utils import create_obj
from server.db import db
from server.core.tests.conftest import staff_headers


ROUTE = "/api/v1/planner"

# TEST GET


#   PLANNER

"""
def test_planner_get(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name="RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=create_recipe(user.id).id,
                date=str(datetime.now().date()),
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        api_route = f"{ROUTE}/{planner.id}"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = planner.to_dict()

        print(result_data)
        # then
        assert response.status_code == 200

        assert result_data["name"] == expected_data["name"]
        assert result_data["owner_user_id"] == expected_data["owner_user_id"]
        assert result_data["is_active"] == expected_data["is_active"]
        assert "items" not in result_data


def test_planner_get_invalid_id(
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


def test_planner_get_authorization(
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
        planner_user_2_not_shared = create_obj(
            RecipePlanner(
                name="RecipePlannerName",
                owner_user_id=user_2.id,
                is_active=True
            )
        )
        planner_user_2_shared_with_user_1 = create_obj(
            RecipePlanner(
                name="RecipePlannerName2",
                owner_user_id=user_2.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner_user_2_shared_with_user_1.id,
                user_id=user.id,
                can_edit=True
            )
        )
        api_route_not_shared = f"{ROUTE}/{planner_user_2_not_shared.id}"
        api_route_shared = f"{ROUTE}/{planner_user_2_shared_with_user_1.id}"

        # when
        unauth_user = client.get(api_route_not_shared)
        user_2_planner_1_owner = client.get(
            api_route_not_shared,
            headers=headers_2
        )
        user_2_planner_2_owner = client.get(
            api_route_shared,
            headers=headers_2
        )
        user_1_planner_1_no_access = client.get(
            api_route_not_shared,
            headers=headers
        )
        user_1_planner_2_access = client.get(
            api_route_shared,
            headers=headers
        )

        # then
        assert unauth_user.status_code != 200
        assert user_2_planner_1_owner.status_code == 200
        assert user_2_planner_2_owner.status_code == 200
        assert user_1_planner_1_no_access.status_code == 401
        assert user_1_planner_2_access.status_code == 200


# TEST GET-LIST

#   PLANNER

def test_planner_get_list(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name="RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=create_recipe(user.id).id,
                date=str(datetime.now().date()),
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        api_route = f"{ROUTE}/{planner.id}"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = planner.to_dict()

        # then
        assert response.status_code == 200

        assert result_data["name"] == expected_data["name"]
        assert result_data["owner_user_id"] == expected_data["owner_user_id"]
        assert result_data["is_active"] == expected_data["is_active"]
        assert "items" not in result_data


def test_planner_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
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


#   Planner Items

def test_planner_item_get_list(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name="RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        api_route = f"{ROUTE}/{planner.id}/item"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = item.to_dict()

        # then
        assert response.status_code == 200
        assert result_data[0]["rplanner_id"] == expected_data["rplanner_id"]
        assert result_data[0]["recipe"]["id"] == expected_data["recipe_id"]
        assert result_data[0]["date"] == str(expected_data["date"])
        assert result_data[0]["label"] == expected_data["label"]
        assert result_data[0]["order_number"] == expected_data["order_number"]
        assert result_data[0]["planned_recipe_person_count"] == expected_data["planned_recipe_person_count"]


def test_planner_items_get_list_query_params(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name="RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        week_1_date = datetime.now().date()  # like today!
        week_2_date = week_1_date + timedelta(days=7)

        recipe = create_recipe(user.id)
        create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(week_1_date),
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(week_1_date),
                label="Frühstück",
                order_number=2,
                planned_recipe_person_count=2
            )
        )
        create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(week_2_date),
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        api_route_today_is_w1 = f"{ROUTE}/{planner.id}/item"
        api_route_w1 = f"{ROUTE}/{planner.id}/item?date_of_week={str(week_1_date)}"
        api_route_w2 = f"{ROUTE}/{planner.id}/item?date_of_week={str(week_2_date)}"

        # when
        response_today_is_w1 = client.get(api_route_today_is_w1, headers=headers)
        response_w1 = client.get(api_route_w1, headers=headers)
        response_w2 = client.get(api_route_w2, headers=headers)

        resp_data_today_is_w1 = json.loads(response_today_is_w1.data)
        resp_data_w1 = json.loads(response_w1.data)
        resp_data_w2 = json.loads(response_w2.data)

        # then
        assert response_today_is_w1.status_code == 200
        assert response_w1.status_code == 200
        assert response_w2.status_code == 200

        assert len(resp_data_today_is_w1) == 2
        assert len(resp_data_w1) == 2
        assert len(resp_data_w2) == 1


def test_planner_item_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        staff_headers: tuple[User, dict],
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_3.id,
                can_edit=False
            )
        )
        create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=create_recipe(user.id).id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        api_route = f"{ROUTE}/{planner.id}/item"

        # when
        response_without = client.get(api_route)
        response_user_owner = client.get(api_route, headers=headers)
        response_user_can_edit = client.get(api_route, headers=headers_2)
        response_user_can_access = client.get(api_route, headers=headers_3)
        response_user_no_access = client.get(api_route, headers=staff_headers)

        resp_user_owner_data = json.loads(response_user_owner.data)
        resp_user_can_edit_data = json.loads(response_user_can_edit.data)
        resp_user_can_access_data = json.loads(response_user_can_access.data)

        # then
        assert response_without.status_code != 200
        assert response_user_owner.status_code == 200
        assert response_user_can_edit.status_code == 200
        assert response_user_can_access.status_code == 200
        assert response_user_no_access.status_code == 401

        assert len(resp_user_owner_data) == 1
        assert len(resp_user_can_edit_data) == 1
        assert len(resp_user_can_access_data) == 1


# TEST-POST

def test_planner_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": "RecipePlannerName",
            "is_active": True
        }
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = RecipePlanner.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()
        expected_data["owner_user_id"] = user.id

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_planner_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": "RecipePlannerName",
            "is_active": True
        }
        api_route = f"{ROUTE}/"

        # when
        response_without = client.post(api_route, json=data)
        response_user = client.post(api_route, headers=headers, json=data)

        # then
        assert response_without.status_code != 201
        assert response_user.status_code == 201


def test_planner_post_invalid_payload(
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
            "name": "RecipePlannerName",
        } # "is_active" not given
        data_name_to_short = {
            "name": "",
            "is_active": True
        } # "name" to short
        data_name_to_long = {
            "name": "T" * 26,
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


#   PLANNER ITEM

def test_planner_item_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        data = {
            "recipe_id": recipe.id,
            "date": str(datetime.now().date()),  # today!,
            "label": "Frühstück",
            "order_number": 1,
            "planned_recipe_person_count": 2
        }
        api_route = f"{ROUTE}/{planner.id}/item"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)

        expected_data = data.copy()

        # then
        assert response.status_code == 201

        assert result_data["rplanner_id"] == planner.id
        assert result_data["recipe"]["id"] == recipe.id
        assert result_data["date"] == str(expected_data["date"])
        assert result_data["label"] == expected_data["label"]
        assert result_data["order_number"] == expected_data["order_number"]
        assert result_data["planned_recipe_person_count"] == expected_data["planned_recipe_person_count"]


def test_planner_item_post_invalid_id(
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


def test_planner_item_post_authorization(
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
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_3.id,
                can_edit=False
            )
        )
        data = {
            "recipe_id": recipe.id,
            "date": str(datetime.now().date()),  # today!,
            "label": "Frühstück",
            "order_number": 1,
            "planned_recipe_person_count": 2
        }
        data_2 = {
            "recipe_id": recipe.id,
            "date": str(datetime.now().date()),  # today!,
            "label": "Frühstück",
            "order_number": 2,
            "planned_recipe_person_count": 2
        }
        api_route = f"{ROUTE}/{planner.id}/item"

        # when
        response_without = client.post(api_route, json=data)
        response_user_owner = client.post(api_route, headers=headers, json=data)
        response_user_shared_with = client.post(api_route, headers=headers_2, json=data_2)
        response_user_access_denied= client.post(api_route, headers=headers_3, json=data_2)

        # then
        assert response_without.status_code != 201
        assert response_user_owner.status_code == 201
        assert response_user_shared_with.status_code == 201
        assert response_user_access_denied.status_code == 401


def test_planner_item_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        duplicate_item: dict = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )

        data_recipe_id_not_existing = {
            "recipe_id": -1,
            "date": str(datetime.now().date()),
            "label": "Frühstück",
            "order_number": 1,
            "planned_recipe_person_count": 2
        }
        data_date_is_null = {
            "recipe_id": 1,
            "label": "Frühstück",
            "order_number": 1,
            "planned_recipe_person_count": 2
        }
        data_invalid_date = {
            "recipe_id": 1,
            "date": "2024-02-",
            "label": "Frühstück",
            "order_number": 1,
            "planned_recipe_person_count": 2
        }
        data_order_number_is_null = {
            "recipe_id": 1,
            "date": str(datetime.now().date()),
            "label": "Frühstück",
            "planned_recipe_person_count": 2
        }
        data_order_number_to_low = {
            "recipe_id": 1,
            "date": str(datetime.now().date()),
            "label": "Frühstück",
            "order_number": 0,
            "planned_recipe_person_count": 2
        }
        data_person_count_is_null = {
            "recipe_id": 1,
            "date": str(datetime.now().date()),
            "order_number": 1,
            "label": "Frühstück"
        }
        data_person_count_to_low = {
            "recipe_id": 1,
            "date": str(datetime.now().date()),
            "label": "Frühstück",
            "order_number": 1,
            "planned_recipe_person_count": 0
        }
        data_duplicate_item = {
            "recipe_id": recipe.id,
            "date": str(datetime.now().date()),  # today!
            "label": "Frühstück",
            "order_number": 1,
            "planned_recipe_person_count": 2
        }
        
        api_route = f"{ROUTE}/{planner.id}/item"

        # when
        resp_recipe_id_not_exisiting = client.post(
            api_route, headers=headers, json=data_recipe_id_not_existing)
        resp_date_is_null = client.post(
            api_route, headers=headers, json=data_date_is_null)
        resp_invalid_date = client.post(
            api_route, headers=headers, json=data_invalid_date)
        resp_order_number_is_null = client.post(
            api_route, headers=headers, json=data_order_number_is_null)
        resp_order_number_to_low = client.post(
            api_route, headers=headers, json=data_order_number_to_low)
        resp_person_count_is_null = client.post(
            api_route, headers=headers, json=data_person_count_is_null)
        resp_person_count_to_low = client.post(
            api_route, headers=headers, json=data_person_count_to_low)
        resp_duplicate_item = client.post(
            api_route, headers=headers, json=data_duplicate_item)

        resp_recipe_id_not_exisiting_data = json.loads(resp_recipe_id_not_exisiting.data)
        resp_date_is_null_data = json.loads(resp_date_is_null.data)
        resp_invalid_date_data = json.loads(resp_invalid_date.data)
        resp_order_number_is_null_data = json.loads(resp_order_number_is_null.data)
        resp_order_number_to_low_data = json.loads(resp_order_number_to_low.data)
        resp_person_count_is_null_data = json.loads(resp_person_count_is_null.data)
        resp_person_count_to_low_data = json.loads(resp_person_count_to_low.data)
        resp_duplicate_item_data = json.loads(resp_duplicate_item.data)

        # then
        assert resp_recipe_id_not_exisiting.status_code == 404
        assert resp_date_is_null.status_code == 400
        assert resp_invalid_date.status_code == 400
        assert resp_order_number_is_null.status_code == 400
        assert resp_order_number_to_low.status_code == 400
        assert resp_person_count_is_null.status_code == 400
        assert resp_person_count_to_low.status_code == 400
        assert resp_duplicate_item.status_code == 409

        assert "message" in resp_recipe_id_not_exisiting_data
        assert "message" in resp_date_is_null_data
        assert "message" in resp_invalid_date_data
        assert "message" in resp_order_number_is_null_data
        assert "message" in resp_order_number_to_low_data
        assert "message" in resp_person_count_is_null_data
        assert "message" in resp_person_count_to_low_data
        assert "message" in resp_duplicate_item_data

        assert "recipe_id" in resp_recipe_id_not_exisiting_data["message"]
        assert "date" in resp_date_is_null_data["message"]
        assert "date" in resp_invalid_date_data["message"]
        assert "order_number" in resp_order_number_is_null_data["message"]
        assert "order_number" in resp_order_number_to_low_data["message"]
        assert "person_count" in resp_person_count_is_null_data["message"]
        assert "person_count" in resp_person_count_to_low_data["message"]
        assert "already existing" in resp_duplicate_item_data["message"]


#   SHARED USER

def test_planner_shared_user_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data = {
            "can_edit": True
        }
        api_route = f"{ROUTE}/{planner.id}/access/user/{user.id}"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = UserSharedRecipePlanner.query.get((planner.id, user.id)).to_dict()

        # then
        assert response.status_code == 201
        assert result_data_db == result_data


def test_planner_shared_user_post_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data = {
            "can_edit": True
        }
        api_route = f"{ROUTE}/100/access/user/{user_2.id}"

        # when
        response = client.post(api_route, headers=headers, json=data)

        # then
        assert response.status_code == 404


def test_planner_shared_user_post_authorization(
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
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        data = {
            "can_edit": True
        }
        api_route = f"{ROUTE}/{planner.id}/access/user/{user_3.id}"

        # when
        response_without = client.post(api_route, json=data)
        response_user_owner = client.post(api_route, headers=headers, json=data)
        response_user_2_shared_edit_but_access_denied = client.post(api_route, headers=headers_2, json=data)
        response_user_3_shared_but_access_denied = client.post(api_route, headers=headers_3, json=data)

        # then
        assert response_without.status_code != 201
        assert response_user_2_shared_edit_but_access_denied.status_code == 401
        assert response_user_owner.status_code == 201
        assert response_user_3_shared_but_access_denied.status_code == 401


def test_planner_shared_user_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data_can_edit_is_null = {}
        api_route = f"{ROUTE}/{planner.id}/access/user/{user.id}"

        # when
        response = client.post(api_route, headers=headers, json=data_can_edit_is_null)
        response_data = json.loads(response.data)

        # then
        assert response.status_code == 400

        assert "message" in response_data
        assert "can_edit" in response_data["message"]


# TEST UPDATE

#   PLANNER

def test_planner_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data = {
            "name": "RecipePlannerUpdatedName",
            "is_active": False
        }
        api_route = f"{ROUTE}/{planner.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = planner.query.get(planner.id).to_dict()

        # then
        assert response.status_code == 200
        assert result_data_db == result_data


def test_planner_patch_invalid_id(
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


def test_planner_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        staff_headers: dict,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_3.id,
                can_edit=False
            )
        )

        data_without = {"name": "NewTestplanner"}
        data_user_owner = {"name": "NewTestplanner2"}
        data_user_2_can_edit = {"name": "NewTestplanner3"}
        data_user_3_access_but_no_edit = {"name": "NewTestplanner4"}
        data_user_staff_access_denied = {"name": "NewTestplanner4"}

        api_route = f"{ROUTE}/{planner.id}"

        # when
        response_without = client.patch(
            api_route, json=data_without)
        response_owner = client.patch(
            api_route, headers=headers, json=data_user_owner)
        response_can_edit = client.patch(
            api_route, headers=headers_2, json=data_user_2_can_edit)
        response_access_but_edit_denied = client.patch(
            api_route, headers=headers_3, json=data_user_3_access_but_no_edit)
        response_access_denied = client.patch(
            api_route, headers=headers_3, json=data_user_staff_access_denied)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 200
        assert response_can_edit.status_code == 200
        assert response_access_but_edit_denied.status_code == 401
        assert response_access_denied.status_code == 401


def test_planner_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    # TODO: WICHTIG -> duplicate testen -> was passiert da?
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        data_name_to_short = {"name": ""}
        data_name_to_long = {"name": "T" * 51}
        data_is_active_is_null = {"is_active": None}
        data_is_owner_user_id_is_readonly = {"owner_user_id": 1}

        api_route = f"{ROUTE}/{planner.id}"

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


#   PLANNER ITEM

def test_planner_item_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name="RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        data = {
            "date": str(datetime.now().date() + timedelta(days=1)),
            "label": "Abendbrot",
            "planned_recipe_person_count": 3,
        }
        api_route = f"{ROUTE}/{planner.id}/item/{planner_item.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = RecipePlannerItem.query.get(planner_item.id).to_dict()

        # then
        print(response.data)
        assert response.status_code == 200
        assert str(result_data["date"]) == data["date"]
        assert result_data["label"] == data["label"]
        assert result_data["planned_recipe_person_count"] == data["planned_recipe_person_count"]


def test_planner_item_patch_invalid_id(
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


def test_planner_item_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        staff_headers: dict,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
        user_3: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    user_3, headers_3 = user_3
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_3.id,
                can_edit=False
            )
        )
        recipe = create_recipe(user.id)
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )

        data = {"label": "new_label"}

        api_route = f"{ROUTE}/{planner.id}/item/{planner_item.id}"

        # when
        response_without = client.patch(
            api_route, json=data)
        response_owner = client.patch(
            api_route, headers=headers, json=data)
        response_can_edit = client.patch(
            api_route, headers=headers_2, json=data)
        response_access_but_edit_denied = client.patch(
            api_route, headers=headers_3, json=data)
        response_no_access = client.patch(
            api_route, headers=staff_headers, json=data)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 200
        assert response_can_edit.status_code == 200
        assert response_access_but_edit_denied.status_code == 401
        assert response_no_access.status_code == 401


def test_planner_item_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        data_quantity_to_low = {"quantity": -1}
        data_is_done_is_null = {"is_done": None}
        api_route = f"{ROUTE}/{planner.id}/item/{planner_item.id}"

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


def test_planner_item_patch_reorder(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        new_order_number = 10
        api_route = f"{ROUTE}/{planner.id}/item/{planner_item.id}/reorder/{new_order_number}"

        # when
        response = client.patch(api_route, headers=headers)
        result_data_db = RecipePlannerItem.query.get(
            json.loads(response.data)["id"]).to_dict()

        # then
        assert response.status_code == 200
        assert result_data_db["order_number"] == new_order_number

    
def test_planner_item_patch_reorder_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        api_route = f"{ROUTE}/{planner.id}/item/{planner_item.id}/reorder/0"

        # when
        response = client.patch(api_route, headers=headers)
        resp_data = json.loads(response.data)

        # then
        assert response.status_code == 400

        assert "message" in resp_data
        assert "order_number" in resp_data["message"]


# TEST DELETE

#   PLANNER

def test_planner_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        db_model_count_before = planner.query.count()
        api_route = f"{ROUTE}/{planner.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = planner.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_planner_delete_invalid_id(
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


def test_planner_delete_authorization(
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
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        planner_2 = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName2",
                owner_user_id=user.id,
                is_active=True
            )
        )

        api_route = f"{ROUTE}/{planner.id}"
        api_route_2 = f"{ROUTE}/{planner_2.id}"

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


#   PLANNER ITEM

def test_planner_item_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        recipe = create_recipe(user.id)
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        db_model_count_before = RecipePlannerItem.query.count()
        api_route = f"{ROUTE}/{planner.id}/item/{planner_item.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = RecipePlannerItem.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_planner_item_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        db_model_count_before = planner.query.count()
        api_route = f"{ROUTE}/{planner.id}/item/-1"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = planner.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_planner_item_delete_authorization(
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
        planner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=planner.id,
                user_id=user_3.id,
                can_edit=False
            )
        )
        recipe = create_recipe(user.id)
        planner_item = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=1,
                planned_recipe_person_count=2
            )
        )
        planner_item_2 = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=2,
                planned_recipe_person_count=2
            )
        )
        planner_item_3 = create_obj(
            RecipePlannerItem(
                rplanner_id=planner.id,
                recipe_id=recipe.id,
                date=str(datetime.now().date()),  # today!
                label="Frühstück",
                order_number=3,
                planned_recipe_person_count=2
            )
        )

        api_route_item_1 = f"{ROUTE}/{planner.id}/item/{planner_item.id}"
        api_route_item_2 = f"{ROUTE}/{planner.id}/item/{planner_item_2.id}"
        api_route_item_3 = f"{ROUTE}/{planner.id}/item/{planner_item_3.id}"

        # when
        response_without = client.delete(api_route_item_1)
        response_owner = client.delete(api_route_item_1, headers=headers)
        response_can_edit = client.delete(api_route_item_2, headers=headers_2)
        response_access_but_no_edit = client.delete(api_route_item_3, headers=headers_3)

        # then
        assert response_without.status_code != 204
        assert response_owner.status_code == 204
        assert response_can_edit.status_code == 204
        assert response_access_but_no_edit.status_code == 401


#   SHARED USER

def test_rplanner_shared_user_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        rplanner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=rplanner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        db_model_count_before = UserSharedRecipePlanner.query.count()
        api_route = f"{ROUTE}/{rplanner.id}/access/user/{user_2.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = UserSharedRecipePlanner.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_rplanner_shared_user_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        rplanner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=rplanner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        db_model_count_before = rplanner.query.count()
        api_route_invalid_rplanner_id = f"{ROUTE}/-1/access/user/{user_2.id}"

        # when
        response_invalid_rplanner_id = client.delete(api_route_invalid_rplanner_id, headers=headers)

        db_model_count_after = rplanner.query.count()

        # then
        assert response_invalid_rplanner_id.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_rplanner_shared_user_delete_authorization(
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
        rplanner = create_obj(
            RecipePlanner(
                name=f"RecipePlannerName",
                owner_user_id=user.id,
                is_active=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=rplanner.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedRecipePlanner(
                rplanner_id=rplanner.id,
                user_id=user_3.id,
                can_edit=False
            )
        )

        api_route = f"{ROUTE}/{rplanner.id}/access/user/{user_2.id}"
        api_route_2 = f"{ROUTE}/{rplanner.id}/access/user/{user_3.id}"

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