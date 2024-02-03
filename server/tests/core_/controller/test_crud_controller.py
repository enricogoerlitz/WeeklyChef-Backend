import pytest

from flask import Flask
from errors import errors

from db import db
from core.models.db_models import (
    Category,
    User,
    RecipeTagComposite,
    Tag,
    Recipe
)
from core.models.api_models import (
    category_model,
    category_model_send, register_model_send,
    recipe_tag_model
)
from core.controller import crud_controller
from core.controller.crud_controller import (
    _check_unqiue_column,
    _ckeck_unique_primarykey,
    _find_object_by_id
)


def create_category(name: str = "TestCategory") -> None:
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()

    return category


def create_user(
        username: str = "TestUsername",
        email: str = "test@email.com",
        password: str = "password"
):
    user = User(
        username=username,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()

    return user


def create_tag(name: str = "TestTag"):
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()

    return tag


def create_recipe(
        creator_user_id: int,
        category_id: int,
        name: str = "TestRecipe",
        person_count: int = 2,
        preperation_description: str = "Test prep desc",
        preperation_time_minutes: int = 25,
        difficulty: str = "fortgeschritten",
        search_description: str = "test recipe",
):
    recipe = Recipe(
        name=name,
        person_count=person_count,
        preperation_description=preperation_description,
        preperation_time_minutes=preperation_time_minutes,
        difficulty=difficulty,
        search_description=search_description,
        creator_user_id=creator_user_id,
        category_id=category_id
    )
    db.session.add(recipe)
    db.session.commit()

    return recipe


# TEST UTILS

# _check_unqiue_column


def test__check_unique_column_success(app: Flask):
    with app.app_context():
        # given
        model_category = Category
        obj_category = model_category.from_json(
            obj={"name": "TestCategory"},
            api_model=category_model_send
        )
        unique_columns_category = ["name"]

        model_user = User
        obj_user = model_user.from_json(
            obj={
                "username": "TestUsername",
                "email": "test@email.com",
                "password": "password"
            },
            api_model=register_model_send
        )
        unique_columns_user = ["username", "email"]

        unique_columns_none = None

        # when + then
        _check_unqiue_column(
            model=model_category,
            obj=obj_category,
            unique_columns=unique_columns_category
        )  # assert no Exception raise

        _check_unqiue_column(
            model=model_user,
            obj=obj_user,
            unique_columns=unique_columns_user
        )  # assert no Exception raise

        _check_unqiue_column(
            model=model_category,
            obj=obj_category,
            unique_columns=unique_columns_none
        )  # assert no Exception raise

        _check_unqiue_column(
            model=model_user,
            obj=obj_user,
            unique_columns=unique_columns_none
        )  # assert no Exception raise


def test__check_unique_column_failed(app: Flask):
    # given
    with app.app_context():
        duplicate_category_name = "TestCategory"
        create_category(duplicate_category_name)
        model_category = Category
        obj_category = model_category.from_json(
            obj={"name": duplicate_category_name},
            api_model=category_model_send
        )
        unique_columns_category = ["name"]

        duplicate_username = "TestUsernameDuplicate"
        duplicate_user_email = "duplicate@user.com"
        create_user(username=duplicate_username)
        create_user(email=duplicate_user_email)
        model_user = User
        obj_user_1 = model_user.from_json(
            obj={
                "username": duplicate_username,
                "email": "no@duplicate.com",
                "password": "password"
            },
            api_model=register_model_send
        )
        obj_user_2 = model_user.from_json(
            obj={
                "username": "TestUsernameNoDuplicate",
                "email": duplicate_user_email,
                "password": "password"
            },
            api_model=register_model_send
        )
        unique_columns_user = ["username", "email"]

        # when + then
        with pytest.raises(errors.DbModelUnqiueConstraintException):
            _check_unqiue_column(
                model=model_category,
                obj=obj_category,
                unique_columns=unique_columns_category
            )

        with pytest.raises(errors.DbModelUnqiueConstraintException):
            _check_unqiue_column(
                model=model_user,
                obj=obj_user_1,
                unique_columns=unique_columns_user
            )

        with pytest.raises(errors.DbModelUnqiueConstraintException):
            _check_unqiue_column(
                model=model_user,
                obj=obj_user_2,
                unique_columns=unique_columns_user
            )


def test__check_unique_primarykey_success(app: Flask):
    with app.app_context():
        # given
        model = Category
        unique_primarykeys = 1

        # when + then
        _ckeck_unique_primarykey(
            model=model,
            unique_primarykeys=unique_primarykeys
        )  # assert no Exception raise


def test__check_unique_primarykey_failed(app: Flask):
    with app.app_context():
        # given
        category = create_category()
        model = Category
        unique_primarykeys = category.id

        # when + then
        with pytest.raises(errors.DbModelAlreadyExistingException):
            _ckeck_unique_primarykey(
                model=model,
                unique_primarykeys=unique_primarykeys
            )


def test__find_object_by_id_success(app: Flask):
    with app.app_context():
        # given
        category = create_category()
        model = Category
        id = category.id

        # when + then
        _find_object_by_id(
            model=model,
            id=id
        )


def test__find_object_by_id_failed(app: Flask):
    with app.app_context():
        # given
        model = Category
        id = 1

        # when + then
        with pytest.raises(errors.DbModelNotFoundException):
            _find_object_by_id(
                model=model,
                id=id
            )


def test_handle_get(app: Flask):
    with app.app_context():
        # given
        category = create_category()
        model = Category
        api_model = category_model
        id = category.id

        # when
        result_data, status_code = crud_controller.handle_get(
            model=model,
            api_model=api_model,
            id=id
        )

        expected_data = category.to_dict()

        # then
        assert status_code == 200
        assert result_data == expected_data


def test_handle_get_not_found(app: Flask):
    with app.app_context():
        # given
        model = Category
        api_model = category_model
        id = -1

        # when
        result_data, status_code = crud_controller.handle_get(
            model=model,
            api_model=api_model,
            id=id
        )

        expected_data = {
            "msg": f"Object {model.__name__} with id = {id} doesn't exist"
        }

        # then
        assert status_code == 404
        assert result_data == expected_data


def test_handle_get_list(app: Flask):
    with app.app_context():
        # given
        model = Category
        api_model = category_model
        categorys = [create_category(f"category{i}") for i in range(0, 3)]

        # when
        result_data, status_code = crud_controller.handle_get_list(
            model=model,
            api_model=api_model
        )

        expected_data = [category.to_dict() for category in categorys]

        # then
        assert status_code == 200
        assert result_data == expected_data


def test_handle_post(app: Flask):
    with app.app_context():
        # given
        model = Category
        api_model = category_model
        api_model_send = category_model_send
        data = {"name": "TestCategory"}
        unique_columns = ["name"]
        unique_primarykey = None

        # when
        result_data, status_code = crud_controller.handle_post(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            data=data,
            unique_columns=unique_columns,
            unique_primarykey=unique_primarykey
        )

        result_data_db = Category.query.filter_by(**data).first().to_dict()
        result_data_without_id = result_data.copy()
        del result_data_without_id["id"]
        expected_data = data.copy()

        # then
        assert status_code == 201
        assert result_data_without_id == expected_data
        assert result_data_db == result_data


def test_handle_post_validation_error(app: Flask):
    with app.app_context():
        # given
        model = Category
        api_model = category_model
        api_model_send = category_model_send
        data = {}
        unique_columns = ["name"]
        unique_primarykey = None

        # when
        result_data, status_code = crud_controller.handle_post(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            data=data,
            unique_columns=unique_columns,
            unique_primarykey=unique_primarykey
        )

        # then
        assert status_code == 400
        assert "msg" in result_data


def test_handle_post_serialization_error(app: Flask):
    with app.app_context():
        # given
        model = Category
        api_model = category_model
        api_model_send = category_model_send
        data = {"AttrNotInModel": ""}
        unique_columns = ["name"]
        unique_primarykey = None

        # when
        result_data, status_code = crud_controller.handle_post(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            data=data,
            unique_columns=unique_columns,
            unique_primarykey=unique_primarykey
        )

        # then
        assert status_code == 400
        assert "msg" in result_data


def test_handle_post_uniquecontraint_error(app: Flask):
    with app.app_context():
        # given
        duplicate_name = "TestCategory"
        create_category(duplicate_name)
        model = Category
        api_model = category_model
        api_model_send = category_model_send
        data = {"name": duplicate_name}
        unique_columns = ["name"]
        unique_primarykey = None

        # when
        result_data, status_code = crud_controller.handle_post(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            data=data,
            unique_columns=unique_columns,
            unique_primarykey=unique_primarykey
        )

        expected_data = {
            "msg": f"Field 'name' with value '{duplicate_name}' is already existing."  # noqa
        }

        # then
        assert status_code == 409
        assert result_data == expected_data


def test_handle_post_alreadyexisting_error(app: Flask):
    with app.app_context():
        # given
        user = create_user()
        category = create_category()
        tag = create_tag()
        recipe = create_recipe(
            creator_user_id=user.id,
            category_id=category.id
        )

        recipe_tag = RecipeTagComposite(recipe_id=recipe.id, tag_id=tag.id)
        db.session.add(recipe_tag)
        db.session.commit()

        model = RecipeTagComposite
        api_model = recipe_tag_model
        api_model_send = recipe_tag_model
        data = {
            "recipe_id": recipe.id,
            "tag_id": tag.id
        }
        unique_columns = None
        unique_primarykey = (recipe.id, tag.id)

        # when
        result_data, status_code = crud_controller.handle_post(
            model=model,
            api_model=api_model,
            api_model_send=api_model_send,
            data=data,
            unique_columns=unique_columns,
            unique_primarykey=unique_primarykey
        )

        # then
        assert status_code == 409
        assert "msg" in result_data


def test_handle_patch(app: Flask):
    with app.app_context():
        # given
        category = create_category()
        model = Category
        api_model = category_model
        id = category.id
        data = {"name": "NewCategoryModelName"}

        # when
        result_data, status_code = crud_controller.handle_patch(
            model=model,
            api_model=api_model,
            id=id,
            data=data
        )

        result_data_db = model.query.get(id).to_dict()
        expected_data = category.to_dict()

        # then
        assert status_code == 200
        assert result_data == expected_data
        assert result_data_db == expected_data


def test_handle_patch_not_found_error(app: Flask):
    with app.app_context():
        # given
        model = Category
        api_model = category_model
        id = -1
        data = {"AttrNotInModel": ""}

        # when
        result_data, status_code = crud_controller.handle_patch(
            model=model,
            api_model=api_model,
            id=id,
            data=data
        )

        # then
        assert status_code == 404
        assert "msg" in result_data


def test_handle_patch_validation_error(app: Flask):
    with app.app_context():
        # given
        category = create_category()
        model = Category
        api_model = category_model
        id = category.id
        data = {"AttrNotInModel": ""}

        # when
        result_data, status_code = crud_controller.handle_patch(
            model=model,
            api_model=api_model,
            id=id,
            data=data
        )

        result_data_db = model.query.get(id).to_dict()
        expected_data = category.to_dict()

        # then
        assert status_code == 400
        assert "msg" in result_data
        assert result_data_db == expected_data


def test_handle_delete(app: Flask):
    with app.app_context():
        # given
        category = create_category()
        model = Category
        id = category.id

        # when
        result_data, status_code = crud_controller.handle_delete(
            model=model,
            id=id
        )

        # then
        assert status_code == 204
        assert result_data is None


def test_handle_delete_not_found_error(app: Flask):
    with app.app_context():
        # given
        model = Category
        id = -1

        # when
        _, status_code = crud_controller.handle_delete(
            model=model,
            id=id
        )

        # then
        assert status_code == 404
