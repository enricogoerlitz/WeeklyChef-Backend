from typing import Any

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from server.db import db
from server.core.utils import model_validator as ModelValidator
from server.utils.decorators import (
    add_to_dict_method,
    add_from_json_method,
    add__str__method
)


@add_from_json_method
@add_to_dict_method
@add__str__method
class Collection(db.Model):
    __tablename__ = "collection"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    owner_user_id = db.Column(db.Integer, nullable=False)  # noqa
    is_default = db.Column(db.Boolean, nullable=False)

    recipes = db.relationship(
        "CollectionRecipeComposite",
        cascade="all,delete",
        backref=db.backref("collection", lazy="select")
    )
    acl = db.relationship(
        "UserSharedCollection",
        cascade="all,delete",
        lazy="select"
    )

    @validates("name")
    def validate_name(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=1,
            max_length=50
        )
        return value

    @validates("owner_user_id")
    def validate_owner_user_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("is_default")
    def validate_is_default(self, key: str, value: Any) -> str:
        ModelValidator.validate_boolean(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class CollectionRecipeComposite(db.Model):
    __tablename__ = "collection_recipe"

    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), primary_key=True)  # noqa
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), primary_key=True)  # noqa

    recipe = db.relationship("Recipe", lazy="select")

    __table_args__ = (
        UniqueConstraint("collection_id", "recipe_id", name="uq_collection_recipe"),  # noqa
    )

    @validates("collection_id")
    def validate_collection_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("recipe_id")
    def validate_recipe_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class UserSharedCollection(db.Model):
    __tablename__ = "collection_user"

    collection_id = db.Column(db.Integer, db.ForeignKey("collection.id"), primary_key=True)  # noqa
    user_id = db.Column(db.Integer, primary_key=True)  # noqa
    can_edit = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        UniqueConstraint("collection_id", "user_id", name="uq_collection_user"),  # noqa
    )

    @validates("collection_id")
    def validate_collection_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("user_id")
    def validate_user_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("can_edit")
    def validate_can_edit(self, key: str, value: Any) -> str:
        ModelValidator.validate_boolean(
            fieldname=key,
            value=value
        )
        return value
