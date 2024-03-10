from typing import Any

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from server.db import db
from server.core.models.db_models.utils import strlen
from server.core.utils import model_validator as ModelValidator
from server.utils.decorators import (
    add_to_dict_method,
    add_from_json_method,
    add__str__method
)


@add_from_json_method
@add_to_dict_method
@add__str__method
class Supermarket(db.Model):
    __tablename__ = "supermarket"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(strlen.L25), nullable=False)
    street = db.Column(db.String(strlen.L100), nullable=False)
    postcode = db.Column(db.String(strlen.L25), nullable=False)
    district = db.Column(db.String(strlen.L50), nullable=False)
    owner_user_id = db.Column(db.Integer, nullable=False)  # noqa

    areas_unsorted = db.relationship(
        "SupermarketArea",
        cascade="all,delete",
        backref="supermarket",
        lazy="dynamic"
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "street",
            name="uq_name_street"
        ),
    )

    @property
    def areas(self):
        return sorted(
            self.areas_unsorted,
            key=lambda x: (x.order_number)
        )

    @validates("name")
    def validate_name(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=3,
            max_length=strlen.L25
        )
        return value

    @validates("street")
    def validate_street(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=3,
            max_length=strlen.L100
        )
        return value

    @validates("postcode")
    def validate_postcode(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=1,
            max_length=strlen.L25
        )
        return value

    @validates("district")
    def validate_district(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=1,
            max_length=strlen.L50
        )
        return value

    @validates("owner_user_id")
    def validate_owner_user_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class SupermarketArea(db.Model):
    __tablename__ = "sarea"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(strlen.L25), unique=True, nullable=False)
    order_number = db.Column(db.Integer, nullable=False)
    supermarket_id = db.Column(db.Integer, db.ForeignKey("supermarket.id"), nullable=False)  # noqa

    ingredients = db.relationship(
        "SupermarketAreaIngredientComposite",
        cascade="all,delete",
        backref="sarea",
        lazy="joined"
    )

    __table_args__ = (
        UniqueConstraint(
            "supermarket_id",
            "name",
            name="uq_supermarketid_name"
        ),
    )

    @validates("name")
    def validate_name(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=3,
            max_length=strlen.L25
        )
        return value

    @validates("order_number")
    def validate_order_number(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value,
            min_=1
        )
        return value

    @validates("supermarket_id")
    def validate_supermarket_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class SupermarketAreaIngredientComposite(db.Model):
    __tablename__ = "sarea_ingredient"

    sarea_id = db.Column(db.Integer, db.ForeignKey("sarea.id"), primary_key=True)  # noqa
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.id"), primary_key=True)  # noqa
    ingredient_price = db.Column(db.Float(precision=2), nullable=False)

    ingredient = db.relationship("Ingredient", lazy="select")

    __table_args__ = (
        UniqueConstraint(
            "sarea_id",
            "ingredient_id",
            name="uq_supermarketid_name"
        ),
    )

    @validates("sarea_id")
    def validate_sarea_id(self, key: str, value: Any) -> str:
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

    @validates("ingredient_price")
    def validate_ingredient_price(self, key: str, value: Any) -> str:
        ModelValidator.validate_float(
            fieldname=key,
            value=value,
            min_=0.
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class UserSharedEditSupermarket(db.Model):
    __tablename__ = "supermarket_edit_user"

    supermarket_id = db.Column(db.Integer, db.ForeignKey("supermarket.id"), primary_key=True)  # noqa
    user_id = db.Column(db.Integer, primary_key=True)  # noqa

    __table_args__ = (
        UniqueConstraint(
            "supermarket_id",
            "user_id",
            name="uq_supermarket_user"
        ),
    )

    @validates("supermarket_id")
    def validate_supermarket_id(self, key: str, value: Any) -> str:
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
