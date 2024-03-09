import json

from flask import Flask, testing

from server.db import db
from server.core.models.db_models.category import Category


ROUTE = "/api/v1/category"


def create_category(name: str = "TestCategory") -> None:
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return category


# TEST GET


def test_category_get(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        category = create_category()
        api_route = f"{ROUTE}/{category.id}"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = category.to_dict()

        # then
        assert response.status_code == 200
        assert result_data == expected_data


def test_category_get_invalid_id(
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


def test_category_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        category = create_category()
        api_route = f"{ROUTE}/{category.id}"

        # when
        response_without = client.get(api_route)
        response_std = client.get(api_route, headers=std_headers)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = category.to_dict()

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST GET-LIST


def test_category_get_list(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        COUNT = 3
        categorys = [create_category(f"category{i}") for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = [category.to_dict() for category in categorys]

        # then
        assert response.status_code == 200
        assert len(categorys) == COUNT
        assert result_data == expected_data


def test_category_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        COUNT = 3
        categorys = [create_category(f"category{i}") for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response_without = client.get(api_route)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)
        response_std = client.get(api_route, headers=std_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = [category.to_dict() for category in categorys]

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST-POST


def test_category_post(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        data = {"name": "TestCategory"}
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Category.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_category_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        data_without = {"name": "TestCategory"}
        data_std = {"name": "TestCategory2"}
        data_staff = {"name": "TestCategory3"}
        data_admin = {"name": "TestCategory4"}
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


def test_category_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
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


def test_category_patch(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        category = create_category()
        data = {"name": "NewCategoryName"}
        api_route = f"{ROUTE}/{category.id}"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Category.query.get(category.id).to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 200
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_category_put_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        data = {"name": "NewCategoryName"}
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        # then
        assert response.status_code == 404


def test_category_put_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        category = create_category()

        data_without = {"name": "NewTestCategory"}
        data_std = {"name": "NewTestCategory2"}
        data_staff = {"name": "NewTestCategory3"}
        data_admin = {"name": "NewTestCategory4"}

        api_route = f"{ROUTE}/{category.id}"

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


def test_category_put_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        category = create_category()

        data_name_to_short = {"name": "T" * 3}  # min 4
        data_name_to_long = {"name": "T" * 31}  # max 30
        api_route = f"{ROUTE}/{category.id}"

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


def test_category_delete(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        category = create_category()
        db_model_count_before = Category.query.count()
        api_route = f"{ROUTE}/{category.id}"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = Category.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_category_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        create_category()
        db_model_count_before = Category.query.count()
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = Category.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_category_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        category_without = create_category("TestCategory")
        category_std = create_category("TestCategory2")
        category_staff = create_category("TestCategory3")
        category_admin = create_category("TestCategory4")

        api_route_without = f"{ROUTE}/{category_without.id}"
        api_route_std = f"{ROUTE}/{category_std.id}"
        api_route_staff = f"{ROUTE}/{category_staff.id}"
        api_route_admin = f"{ROUTE}/{category_admin.id}"

        # when
        response_without = client.delete(api_route_without)
        response_std = client.delete(api_route_std, headers=std_headers)
        response_staff = client.delete(api_route_staff, headers=staff_headers)
        response_admin = client.delete(api_route_admin, headers=admin_headers)

        result_data_db_without = Category.query.get(category_without.id)
        result_data_db_std = Category.query.get(category_std.id)
        result_data_db_staff = Category.query.get(category_staff.id)
        result_data_db_admin = Category.query.get(category_admin.id)

        # then
        assert response_without.status_code != 204
        assert response_std.status_code == 401
        assert response_staff.status_code == 204
        assert response_admin.status_code == 204

        assert result_data_db_without is not None
        assert result_data_db_std is not None
        assert result_data_db_staff is None
        assert result_data_db_admin is None
