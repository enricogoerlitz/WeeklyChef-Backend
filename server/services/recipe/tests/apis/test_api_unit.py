# flake8: noqa
import json

from flask import Flask, testing

from server.db import db
from server.core.models.db_models.unit import Unit


ROUTE = "/api/v1/unit"


def create_unit(name: str = "TestUnit") -> None:
    unit = Unit(name=name)
    db.session.add(unit)
    db.session.commit()

    return unit


# TEST GET

"""
def test_unit_get(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        api_route = f"{ROUTE}/{unit.id}"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = unit.to_dict()

        # then
        assert response.status_code == 200
        assert result_data == expected_data


def test_unit_get_invalid_id(
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


def test_unit_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        api_route = f"{ROUTE}/{unit.id}"

        # when
        response_without = client.get(api_route)
        response_std = client.get(api_route, headers=std_headers)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = unit.to_dict()

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST GET-LIST


def test_unit_get_list(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        COUNT = 3
        units = [create_unit(f"unit{i}") for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response = client.get(api_route, headers=admin_headers)

        result_data = json.loads(response.data)
        expected_data = [unit.to_dict() for unit in units]

        # then
        assert response.status_code == 200
        assert len(units) == COUNT
        assert result_data == expected_data


def test_unit_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        COUNT = 3
        units = [create_unit(f"unit{i}") for i in range(0, COUNT)]
        api_route = f"{ROUTE}/"

        # when
        response_without = client.get(api_route)
        response_staff = client.get(api_route, headers=staff_headers)
        response_admin = client.get(api_route, headers=admin_headers)
        response_std = client.get(api_route, headers=std_headers)

        result_data_std = json.loads(response_std.data)
        result_data_staff = json.loads(response_staff.data)
        result_data_admin = json.loads(response_admin.data)
        expected_data = [unit.to_dict() for unit in units]

        # then
        assert response_without.status_code != 200
        assert response_std.status_code == 200
        assert response_staff.status_code == 200
        assert response_admin.status_code == 200

        assert result_data_std == expected_data
        assert result_data_staff == expected_data
        assert result_data_admin == expected_data


# TEST-POST


def test_unit_post(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        data = {"name": "TestUnit"}
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Unit.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_unit_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        data_without = {"name": "TestUnit"}
        data_std = {"name": "TestUnit2"}
        data_staff = {"name": "TestUnit3"}
        data_admin = {"name": "TestUnit4"}
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


def test_unit_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        data_name_is_null = {}                  # "name" not given
        data_name_to_short = {"name": ""}
        data_name_to_long = {"name": "T" * 26}  # max 30
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


def test_unit_patch(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        data = {"name": "NewUnitName"}
        api_route = f"{ROUTE}/{unit.id}"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Unit.query.get(unit.id).to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert response.status_code == 200
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_unit_patch_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        data = {"name": "NewUnitName"}
        api_route = f"{ROUTE}/-1"

        # when
        response = client.patch(api_route, headers=admin_headers, json=data)

        # then
        assert response.status_code == 404


def test_unit_patch_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()

        data_without = {"name": "NewTestUnit"}
        data_std = {"name": "NewTestUnit2"}
        data_staff = {"name": "NewTestUnit3"}
        data_admin = {"name": "NewTestUnit4"}

        api_route = f"{ROUTE}/{unit.id}"

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


def test_unit_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()

        data_name_to_short = {"name": ""}
        data_name_to_long = {"name": "T" * 26}  # max 30
        api_route = f"{ROUTE}/{unit.id}"

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


def test_unit_delete(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit = create_unit()
        db_model_count_before = Unit.query.count()
        api_route = f"{ROUTE}/{unit.id}"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = Unit.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_unit_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        admin_headers: dict
):
    with app.app_context():
        # given
        create_unit()
        db_model_count_before = Unit.query.count()
        api_route = f"{ROUTE}/-1"

        # when
        response = client.delete(api_route, headers=admin_headers)

        db_model_count_after = Unit.query.count()

        # then
        assert response.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_unit_delete_authorization(
        app: Flask,
        client: testing.FlaskClient,
        std_headers: dict,
        staff_headers: dict,
        admin_headers: dict
):
    with app.app_context():
        # given
        unit_without = create_unit("TestUnit")
        unit_std = create_unit("TestUnit2")
        unit_staff = create_unit("TestUnit3")
        unit_admin = create_unit("TestUnit4")

        api_route_without = f"{ROUTE}/{unit_without.id}"
        api_route_std = f"{ROUTE}/{unit_std.id}"
        api_route_staff = f"{ROUTE}/{unit_staff.id}"
        api_route_admin = f"{ROUTE}/{unit_admin.id}"

        # when
        response_without = client.delete(api_route_without)
        response_std = client.delete(api_route_std, headers=std_headers)
        response_staff = client.delete(api_route_staff, headers=staff_headers)
        response_admin = client.delete(api_route_admin, headers=admin_headers)

        result_data_db_without = Unit.query.get(unit_without.id)
        result_data_db_std = Unit.query.get(unit_std.id)
        result_data_db_staff = Unit.query.get(unit_staff.id)
        result_data_db_admin = Unit.query.get(unit_admin.id)

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