from typing import Any

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from server.db import db
from server.errors import errors
from server.core.enums import difficulty
from server.core.utils import model_validator as ModelValidator
from server.utils.decorators import (
    add_to_dict_method,
    add_from_json_method,
    add__str__method
)
from server.logger import logger


@add_from_json_method
@add_to_dict_method
@add__str__method
class Recipe(db.Model):
    __tablename__ = "recipe"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    person_count = db.Column(db.Integer, nullable=False)
    preperation_description = db.Column(db.String(1_000), nullable=False)
    preperation_time_minutes = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(15), nullable=False)
    search_description = db.Column(db.String(75), nullable=False)

    creator_user_id = db.Column(db.Integer, nullable=False)  # noqa
    # creator_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # noqa
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)  # noqa

    category = db.relationship("Category", backref="recipe", lazy="select")
    ingredients = db.relationship(
        "RecipeIngredient",
        backref=db.backref("recipe", lazy="select")
    )
    tags = db.relationship(
        "Tag",
        secondary="recipe_tag",
        backref=db.backref("recipe", lazy="dynamic")
    )
    images = db.relationship(
        "RecipeImage",
        secondary="recipe_image",
        backref=db.backref("recipe", lazy="dynamic")
    )

    @validates("name")
    def validate_name(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=5,
            max_length=50
        )
        return value

    @validates("person_count")
    def validate_person_count(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value,
            min_=1,
            max_=100
        )
        return value

    @validates("preperation_description")
    def validate_preperation_description(
        self,
        key: str,
        value: Any
    ) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=5,
            max_length=1_000
        )
        return value

    @validates("preperation_time_minutes")
    def validate_preperation_time_minutes(
        self,
        key: str,
        value: Any
    ) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value,
            min_=1,
            max_=100_000
        )
        return value

    @validates("difficulty")
    def validate_difficulty(self, _: str, value: Any) -> str:
        if str(value) not in difficulty.ALLOWED_DIFFICULTIES:
            logger.error(value)
            err_msg = "The field 'difficulty' must be 'einfach', 'normal' or 'fortgeschritten''"  # noqa
            raise errors.DbModelValidationException(err_msg)
        return value

    @validates("search_description")
    def validate_search_description(self, key: str, value: str) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=4,
            max_length=75
        )
        return value

    @validates("creator_user_id")
    def validate_creator_user_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("category_id")
    def validate_category_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredient"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)  # noqa
    quantity = db.Column(db.Integer, nullable=False)

    ingredient = db.relationship(
        "Ingredient",
        backref=db.backref("recipe_ingredient", lazy="dynamic")
    )

    __table_args__ = (
        UniqueConstraint("recipe_id", "ingredient_id", name="uq_recipe_ingredient"),  # noqa
    )

    @validates("recipe_id")
    def validate_recipe_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("ingredient_id")
    def validate_ingredient_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("quantity")
    def validate_quantity(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value,
            min_=1,
            max_=100_000
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class RecipeTagComposite(db.Model):
    __tablename__ = "recipe_tag"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), primary_key=True)  # noqa

    __table_args__ = (
        UniqueConstraint("recipe_id", "tag_id", name="uq_recipe_tag"),  # noqa
    )

    @validates("recipe_id")
    def validate_recipe_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("tag_id")
    def validate_tag_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class RecipeRating(db.Model):
    __tablename__ = "recipe_rating"

    user_id = db.Column(db.Integer, primary_key=True)  # noqa
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    rating = db.Column(db.Float(precision=2), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "recipe_id", name="uq_user_recipe_rating"),  # noqa
    )

    @validates("user_id")
    def validate_user_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("recipe_id")
    def validate_tag_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("rating")
    def validate_rating(self, key: str, value: Any) -> str:
        ModelValidator.validate_float(
            fieldname=key,
            value=value,
            min_=0.5,
            max_=5
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class RecipeImage(db.Model):
    __tablename__ = "rimage"

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), unique=True, nullable=False)

    @validates("path")
    def validate_path(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=3,
            max_length=1_000,
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class ReicpeImageComposite(db.Model):
    __tablename__ = "recipe_image"

    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa
    image_id = db.Column(db.Integer, db.ForeignKey("rimage.id"), primary_key=True)  # noqa

    __table_args__ = (
        UniqueConstraint("recipe_id", "image_id", name="uq_recipe_image"),  # noqa
    )

    @validates("recipe_id")
    def validate_tag_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("image_id")
    def validate_image_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value
