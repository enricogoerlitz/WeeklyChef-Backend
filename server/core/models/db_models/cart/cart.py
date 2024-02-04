"""


Jeder hat einen Einkaufkorb
Die Einkäufskörbe können aber freigegeben werden
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
    name = db.Column(db.String(30), unique=True, nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # noqa
    is_active = db.Column(db.Boolean, nullable=False, default=True)

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


class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=True)  # noqa can be NULL!!!
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), nullable=False)  # noqa
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # noqa
    quantity = db.Column(db.Integer, nullable=False)
    is_done = db.Column(db.Boolean, nullable=False)

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

    @validates("owner_user_id")
    def validate_owner_user_id(self, key: str, value: Any) -> str:
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
class UserSharedCart(db.Model):
    """
    Extra Route für planner/shared -> retuns list of Planner shared with me
    """
    __tablename__ = "cart_user"

    rplanner_id = db.Column(db.Integer, db.ForeignKey("rplanner.id"), primary_key=True)  # noqa
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # noqa
    can_edit = db.Column(db.Boolean, nullable=False)

    planner = db.relationship("RecipePlanner", backref="cart_user", lazy="select")  # noqa

    __table_args__ = (
        UniqueConstraint("rplanner_id", "user_id", name="uq_rplanner_user"),
    )

    @validates("rplanner_id")
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

    @validates("can_edit")
    def validate_can_edit(self, key: str, value: Any) -> str:
        ModelValidator.validate_boolean(
            fieldname=key,
            value=value
        )
        return value
