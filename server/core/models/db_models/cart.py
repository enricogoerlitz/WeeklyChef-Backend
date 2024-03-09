"""


Jeder hat einen Einkaufkorb
Die Einkäufskörbe können aber freigegeben werden

Ein Item im Einkaufskorb entspricht einem Ingredient!
    - dieses kann, muss aber nicht, zu einem Rezept gehören
"""

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
class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    owner_user_id = db.Column(db.Integer, nullable=False)  # noqa
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    items = db.relationship("CartItem", lazy="dynamic")

    __table_args__ = (
        UniqueConstraint("name", "owner_user_id", name="uq_cart_name_user"),
    )

    @validates("name")
    def validate_name(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=1,
            max_length=30
        )
        return value

    @validates("owner_user_id")
    def validate_owner_user_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("is_active")
    def validate_is_active(self, key: str, value: Any) -> str:
        ModelValidator.validate_boolean(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=True)  # noqa can be NULL!!!
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), nullable=False)  # noqa
    quantity = db.Column(db.Integer, nullable=False)
    is_done = db.Column(db.Boolean, nullable=False)

    recipe = db.relationship("Recipe", lazy="select")
    ingredient = db.relationship("Ingredient", lazy="select")

    @validates("cart_id")
    def validate_cart_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value

    @validates("recipe_id")
    def validate_recipe_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value,
            nullable=True
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
            min_=0
        )
        return value

    @validates("is_done")
    def validate_is_done(self, key: str, value: Any) -> str:
        ModelValidator.validate_boolean(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class UserSharedEditCart(db.Model):
    """
    Extra Route für planner/shared -> retuns list of Planner shared with me
    """
    __tablename__ = "cart_user"

    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), primary_key=True)  # noqa
    user_id = db.Column(db.Integer, primary_key=True)  # noqa

    __table_args__ = (
        UniqueConstraint("cart_id", "user_id", name="uq_rplanner_user"),
    )

    @validates("cart_id")
    def validate_rplanner_id(self, key: str, value: Any) -> str:
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
