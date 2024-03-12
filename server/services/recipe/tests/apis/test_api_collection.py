# flake8: noqa
import json

from flask import Flask, testing
import server.core.models.db_models
from server.core.models.db_models.collection import (
    Collection, CollectionRecipeComposite, UserSharedCollection
)
from server.core.models.db_models.user.user import User
from server.services.recipe.tests.apis.test_api_ingredient import (
    create_ingredient
)
from server.services.recipe.tests.apis.test_api_recipe import create_recipe, create_recipe_in_loop
from server.services.recipe.tests.utils import create_obj
from server.services.recipe.tests.apis.test_api_category import create_category


ROUTE = "/api/v1/collection"


# TEST GET


#   COLLECTION
"""
def test_collection_get(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name="CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        recipe = create_recipe(user.id)
        create_obj(
            CollectionRecipeComposite(
                collection_id=collection.id,
                recipe_id=recipe.id
            )
        )
        api_route = f"{ROUTE}/{collection.id}"

        # when
        response = client.get(api_route, headers=headers)

        result_data = json.loads(response.data)
        expected_data = collection.to_dict()
        expected_data["recipes"] = [recipe]

        # then
        assert response.status_code == 200

        assert result_data["name"] == expected_data["name"]
        assert result_data["owner_user_id"] == expected_data["owner_user_id"]
        assert result_data["is_default"] == expected_data["is_default"]
        assert len(result_data["recipes"]) == len(expected_data["recipes"])
        assert result_data["recipes"][0]["id"] == recipe.id


def test_collection_get_invalid_id(
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


def test_collection_get_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2

    with app.app_context():
        # given
        collection_user_2_not_shared = create_obj(
            Collection(
                name="CollectionName",
                owner_user_id=user_2.id,
                is_default=True
            )
        )
        collection_user_2_shared_with_user_1 = create_obj(
            Collection(
                name="CollectionName2",
                owner_user_id=user_2.id,
                is_default=True
            )
        )
        user_shared = create_obj(
            UserSharedCollection(
                collection_id=collection_user_2_shared_with_user_1.id,
                user_id=user.id,
                can_edit=False
            )
        )
        api_route_not_shared = f"{ROUTE}/{collection_user_2_not_shared.id}"
        api_route_shared = f"{ROUTE}/{collection_user_2_shared_with_user_1.id}"

        # when
        unauth_user = client.get(api_route_not_shared)
        user_2_collection_1_access = client.get(
            api_route_not_shared,
            headers=headers_2
        )
        user_2_collection_2_access = client.get(
            api_route_shared,
            headers=headers_2
        )
        user_1_collection_1_no_access = client.get(
            api_route_not_shared,
            headers=headers
        )
        user_1_collection_2_access = client.get(
            api_route_shared,
            headers=headers
        )

        user_2_collection_1_data = json.loads(user_2_collection_1_access.data)
        user_2_collection_2_data = json.loads(user_2_collection_2_access.data)
        user_1_collection_2_data = json.loads(user_1_collection_2_access.data)

        collection_1_expected_data = collection_user_2_not_shared.to_dict()
        collection_2_expected_data = collection_user_2_shared_with_user_1.to_dict()

        del collection_1_expected_data["recipes_"]
        del collection_2_expected_data["recipes_"]
        collection_1_expected_data["recipes"] = []
        collection_1_expected_data["acl"] = []
        collection_2_expected_data["recipes"] = []
        collection_2_expected_data["acl"] = [user_shared.to_dict()]
        del collection_2_expected_data["acl"][0]["collection_id"]

        # then
        assert unauth_user.status_code != 200
        assert user_2_collection_1_access.status_code == 200
        assert user_2_collection_2_access.status_code == 200
        assert user_1_collection_1_no_access.status_code == 401
        assert user_1_collection_2_access.status_code == 200

        assert user_2_collection_1_data == collection_1_expected_data
        assert user_2_collection_2_data == collection_2_expected_data
        assert user_1_collection_2_data == collection_2_expected_data


# TEST GET-LIST

#   COLLECTION

def test_collection_get_list(
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
        collections_user_1 = [
            create_obj(
                Collection(
                    name=f"CollectionName{i}",
                    owner_user_id=user.id,
                    is_default=True
                )
            )
                for i in range(0, COUNT)
        ]
        collection_user_2 = create_obj(
            Collection(
                name=f"CollectionName{COUNT + 1}",
                owner_user_id=user_2.id,
                is_default=True
            )
        )
        collection_user_3 = create_obj(
            Collection(
                name=f"CollectionName{COUNT + 2}",
                owner_user_id=user_3.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collections_user_1[0].id,
                user_id=user_2.id,
                can_edit=False
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

        expected_data_user_1 = [collection.to_dict() for collection in collections_user_1]
        expected_data_user_2 = [collections_user_1[0], collection_user_2]
        expected_data_user_3 = [collection_user_3.to_dict()]
        
        expected_collection_data_1 = collections_user_1[0].to_dict()

        # then
        assert response.status_code == 200
        assert response_2.status_code == 200
        assert response_3.status_code == 200

        assert len(result_data_user_1) == len(expected_data_user_1)
        assert len(result_data_user_2) == len(expected_data_user_2)
        assert len(result_data_user_3) == len(expected_data_user_3)

        assert result_data_user_1[0]["name"] == expected_collection_data_1["name"]
        assert result_data_user_1[0]["owner_user_id"] == expected_collection_data_1["owner_user_id"]
        assert result_data_user_1[0]["is_default"] == expected_collection_data_1["is_default"]


def test_collection_get_list_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
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

def test_collection_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": "CollectionName",
            "is_default": True
        }
        api_route = f"{ROUTE}/"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = Collection.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()
        expected_data["owner_user_id"] = user.id

        del result_data_without_id["recipes"]
        del result_data_without_id["acl"]
        del result_data["recipes"]
        del result_data["acl"]

        # then
        assert response.status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_collection_post_authorization(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data = {
            "name": "CollectionName",
            "is_default": True
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


def test_collection_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        data_name_is_null = {
            "is_default": True
        } # "name" not given
        data_is_default_is_null = {
            "name": "CollectionName",
        } # "is_default" not given
        data_name_to_short = {
            "name": "",
            "is_default": True
        } # "name" to short
        data_name_to_long = {
            "name": "T" * 51,
            "is_default": True
        } # "name" to long

        api_route = f"{ROUTE}/"

        # when
        response_name_is_null = client.post(
            api_route, headers=headers, json=data_name_is_null)
        response_is_default_is_null = client.post(
            api_route, headers=headers, json=data_is_default_is_null)
        response_name_to_short = client.post(
            api_route, headers=headers, json=data_name_to_short)
        response_name_to_long = client.post(
            api_route, headers=headers, json=data_name_to_long)

        response_name_is_null_data = json.loads(response_name_is_null.data)
        response_is_default_is_null_data = json.loads(response_is_default_is_null.data)
        response_name_to_short_data = json.loads(response_name_to_short.data)
        response_name_to_long_data = json.loads(response_name_to_long.data)

        # then
        assert response_name_is_null.status_code == 400
        assert response_is_default_is_null.status_code == 400
        assert response_name_to_short.status_code == 400
        assert response_name_to_long.status_code == 400

        assert "message" in response_name_is_null_data
        assert "message" in response_is_default_is_null_data
        assert "message" in response_name_to_short_data
        assert "message" in response_name_to_long_data

        assert "name" in response_name_is_null_data["message"]
        assert "is_default" in response_is_default_is_null_data["message"]
        assert "name" in response_name_to_short_data["message"]
        assert "name" in response_name_to_long_data["message"]


#   COLLECTION RECIPE

def test_collection_recipe_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        recipe = create_recipe(user.id)
        api_route = f"{ROUTE}/{collection.id}/recipe/{recipe.id}"

        # when
        response = client.post(api_route, headers=headers)

        response_data = json.loads(response.data)
        result_data_db = CollectionRecipeComposite.query.get((collection.id, recipe.id)).to_dict()

        # then
        assert response.status_code == 201

        assert response_data == result_data_db


def test_collection_recipe_post_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )

        api_route_recipe_id_invalid = f"{ROUTE}/100/recipe/1"
        api_route_collection_id_invalid = f"{ROUTE}/{collection.id}/recipe/1"

        # when
        response = client.post(api_route_recipe_id_invalid, headers=headers)
        response_2 = client.post(api_route_collection_id_invalid, headers=headers)

        response_data = json.loads(response.data)
        response_data_2 = json.loads(response_2.data)

        # then
        assert response.status_code == 404
        assert response_2.status_code == 404

        assert "message" in response_data
        assert "message" in response_data_2


def test_collection_recipe_post_authorization(
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
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        category = create_category()
        recipes = [create_recipe_in_loop(i, user.id, category) for i in range(0, 3)]
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_3.id,
                can_edit=False
            )
        )
        api_route = f"{ROUTE}/{collection.id}/recipe/{recipes[0].id}"
        api_route_2 = f"{ROUTE}/{collection.id}/recipe/{recipes[1].id}"
        api_route_3 = f"{ROUTE}/{collection.id}/recipe/{recipes[2].id}"

        # when
        response_without = client.post(api_route)
        response_user_owner = client.post(api_route, headers=headers)
        response_user_shared_with_edit = client.post(api_route_2, headers=headers_2)
        response_user_shared_with_no_edit = client.post(api_route_3, headers=headers_3)
        response_user_shared_with_no_access = client.post(api_route_3, headers=headers_3)

        # then
        assert response_without.status_code != 201
        assert response_user_owner.status_code == 201
        assert response_user_shared_with_edit.status_code == 201
        assert response_user_shared_with_no_edit.status_code == 401
        assert response_user_shared_with_no_access.status_code == 401


#   SHARED USER

def test_collection_shared_user_post(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        data = {
            "can_edit": True
        }
        api_route = f"{ROUTE}/{collection.id}/access/user/{user.id}"

        # when
        response = client.post(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = UserSharedCollection.query.get((collection.id, user.id)).to_dict()

        # then
        assert response.status_code == 201
        assert result_data_db == result_data


def test_collection_shared_user_post_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
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


def test_collection_shared_user_post_authorization(
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
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        data = {
            "can_edit": True
        }
        api_route = f"{ROUTE}/{collection.id}/access/user/{user_3.id}"

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


def test_collection_shared_user_post_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        data_can_edit_is_null = {}
        api_route = f"{ROUTE}/{collection.id}/access/user/{user.id}"

        # when
        response = client.post(api_route, headers=headers, json=data_can_edit_is_null)
        response_data = json.loads(response.data)

        # then
        assert response.status_code == 400

        assert "message" in response_data
        assert "can_edit" in response_data["message"]


# TEST UPDATE

#   COLLECTION

def test_collection_patch(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        data = {
            "name": "CollectionUpdatedName",
            "is_default": False
        }
        api_route = f"{ROUTE}/{collection.id}"

        # when
        response = client.patch(api_route, headers=headers, json=data)

        result_data = json.loads(response.data)
        result_data_db = collection.query.get(collection.id).to_dict()
        del result_data_db["recipes_"]
        result_data_db["recipes"] = []

        # then
        assert response.status_code == 200
        assert result_data_db == result_data


def test_collection_patch_invalid_id(
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


def test_collection_patch_authorization(
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
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_3.id,
                can_edit=False
            )
        )

        data_without = {"name": "NewTestcollection"}
        data_user_owner = {"name": "NewTestcollection2"}
        data_user_2_can_edit = {"name": "NewTestcollection3"}
        data_user_3_has_access_but_denied = {"name": "NewTestcollection4"}

        api_route = f"{ROUTE}/{collection.id}"

        # when
        response_without = client.patch(
            api_route, json=data_without)
        response_owner = client.patch(
            api_route, headers=headers, json=data_user_owner)
        response_can_edit = client.patch(
            api_route, headers=headers_2, json=data_user_2_can_edit)
        response_access_denied = client.patch(
            api_route, headers=headers_3, json=data_user_3_has_access_but_denied)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 200
        assert response_can_edit.status_code == 200
        assert response_access_denied.status_code == 401


def test_collection_patch_invalid_payload(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        data_name_to_short = {"name": ""}
        data_name_to_long = {"name": "T" * 51}
        data_is_default_is_null = {"is_default": None}
        data_is_owner_user_id_is_readonly = {"owner_user_id": 1}

        api_route = f"{ROUTE}/{collection.id}"

        # when
        resp_name_to_short = client.patch(api_route, headers=headers, json=data_name_to_short)
        resp_name_to_long = client.patch(api_route, headers=headers, json=data_name_to_long)
        resp_is_default_is_null = client.patch(api_route, headers=headers, json=data_is_default_is_null)
        resp_is_owner_user_id_is_readonly = client.patch(api_route, headers=headers, json=data_is_owner_user_id_is_readonly)

        resp_name_to_short_data = json.loads(resp_name_to_short.data)
        resp_name_to_long_data = json.loads(resp_name_to_long.data)
        resp_is_default_is_null_data = json.loads(resp_is_default_is_null.data)
        resp_is_owner_user_id_is_readonly_data = json.loads(resp_is_owner_user_id_is_readonly.data)

        # then
        assert resp_name_to_short.status_code == 400
        assert resp_name_to_long.status_code == 400
        assert resp_is_default_is_null.status_code == 400
        assert resp_is_owner_user_id_is_readonly.status_code == 400

        assert "message" in resp_name_to_short_data
        assert "message" in resp_name_to_long_data
        assert "message" in resp_is_default_is_null_data
        assert "message" in resp_is_owner_user_id_is_readonly_data

        assert "name" in resp_name_to_short_data["message"]
        assert "name" in resp_name_to_long_data["message"]
        assert "is_default" in resp_is_default_is_null_data["message"]
        assert "owner_user_id" in resp_is_owner_user_id_is_readonly_data["message"]
        assert "read only" in resp_is_owner_user_id_is_readonly_data["message"]


# TEST DELETE

#   COLLECTION

def test_collection_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        db_model_count_before = collection.query.count()
        api_route = f"{ROUTE}/{collection.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = collection.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_collection_delete_invalid_id(
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


def test_collection_delete_authorization(
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
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_3.id,
                can_edit=False
            )
        )

        api_route = f"{ROUTE}/{collection.id}"

        # when
        response_without = client.delete(api_route)
        response_can_edit_but_not_delete = client.delete(api_route, headers=headers_2)
        response_can_access_but_not_delete = client.delete(api_route, headers=headers_3)
        response_owner = client.delete(api_route, headers=headers)

        # then
        assert response_without.status_code != 200
        assert response_owner.status_code == 204
        assert response_can_edit_but_not_delete.status_code == 401
        assert response_can_access_but_not_delete.status_code == 401


#   COLLECTION RECIPE

def test_collection_recipe_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        recipe = create_recipe(user.id)
        create_obj(
            CollectionRecipeComposite(
                collection_id=collection.id,
                recipe_id=recipe.id
            )
        )
        db_model_count_before = CollectionRecipeComposite.query.count()
        api_route = f"{ROUTE}/{collection.id}/recipe/{recipe.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = CollectionRecipeComposite.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_collection_recipe_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict]
):
    user, headers = user
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        db_model_count_before = collection.query.count()
        api_route = f"{ROUTE}/-1/recipe/-1"
        api_route_2 = f"{ROUTE}/{collection.id}/recipe/-1"

        # when
        response = client.delete(api_route, headers=headers)
        response_2 = client.delete(api_route_2, headers=headers)

        db_model_count_after = collection.query.count()

        # then
        assert response.status_code == 404
        assert response_2.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_collection_recipe_delete_authorization(
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
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_3.id,
                can_edit=False
            )
        )
        category = create_category()
        recipes = [create_recipe_in_loop(i, user.id, category) for i in range(0, 3)]

        create_obj(
            CollectionRecipeComposite(
                collection_id=collection.id,
                recipe_id=recipes[0].id
            )
        )
        create_obj(
            CollectionRecipeComposite(
                collection_id=collection.id,
                recipe_id=recipes[1].id
            )
        )
        create_obj(
            CollectionRecipeComposite(
                collection_id=collection.id,
                recipe_id=recipes[2].id
            )
        )

        api_route_recipe_1 = f"{ROUTE}/{collection.id}/recipe/{recipes[0].id}"
        api_route_recipe_2 = f"{ROUTE}/{collection.id}/recipe/{recipes[1].id}"
        api_route_recipe_3 = f"{ROUTE}/{collection.id}/recipe/{recipes[2].id}"

        # when
        response_without = client.delete(api_route_recipe_1)
        response_owner = client.delete(api_route_recipe_1, headers=headers)
        response_can_edit = client.delete(api_route_recipe_2, headers=headers_2)
        response_access_denied = client.delete(api_route_recipe_3, headers=headers_3)

        # then
        assert response_without.status_code != 204
        assert response_owner.status_code == 204
        assert response_can_edit.status_code == 204
        assert response_access_denied.status_code == 401


#   SHARED USER

def test_collection_shared_user_delete(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict],
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        db_model_count_before = UserSharedCollection.query.count()
        api_route = f"{ROUTE}/{collection.id}/access/user/{user_2.id}"

        # when
        response = client.delete(api_route, headers=headers)

        db_model_count_after = UserSharedCollection.query.count()

        # then
        assert response.status_code == 204
        assert db_model_count_before == 1
        assert db_model_count_after == 0


def test_collection_shared_user_delete_invalid_id(
        app: Flask,
        client: testing.FlaskClient,
        user: tuple[User, dict],
        user_2: tuple[User, dict]
):
    user, headers = user
    user_2, headers_2 = user_2
    with app.app_context():
        # given
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        db_model_count_before = collection.query.count()
        api_route_invalid_collection_id = f"{ROUTE}/-1/access/user/{user_2.id}"

        # when
        response_invalid_collection_id = client.delete(api_route_invalid_collection_id, headers=headers)

        db_model_count_after = collection.query.count()

        # then
        assert response_invalid_collection_id.status_code == 404
        assert db_model_count_before == 1
        assert db_model_count_after == 1


def test_collection_shared_user_delete_authorization(
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
        collection = create_obj(
            Collection(
                name=f"CollectionName",
                owner_user_id=user.id,
                is_default=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_2.id,
                can_edit=True
            )
        )
        create_obj(
            UserSharedCollection(
                collection_id=collection.id,
                user_id=user_3.id,
                can_edit=False
            )
        )

        api_route = f"{ROUTE}/{collection.id}/access/user/{user_2.id}"
        api_route_2 = f"{ROUTE}/{collection.id}/access/user/{user_3.id}"

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