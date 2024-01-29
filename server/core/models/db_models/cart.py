"""
Cart models


Jeder hat einen Einkaufkorb
Die Einkäufskörbe können aber freigegeben werden
"""

from typing import Any

# from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from db import db
from utils import model_validator as ModelValidator
from utils.decorators import (
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
    name = db.Column(db.String(10), unique=True, nullable=False)
    owner_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # noqa
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    @validates("name")
    def validate_unitname(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=1,
            max_length=10
        )
        return value

    def __str__(self) -> str:
        return str(dict(self))


class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"))
    is_done = db.Column(db.Boolean, nullable=False)
