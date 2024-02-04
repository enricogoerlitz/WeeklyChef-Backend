from typing import Any

from sqlalchemy.orm import validates

from db import db
from core.utils import model_validator as ModelValidator
from utils.decorators import (
    add_to_dict_method,
    add_from_json_method,
    add__str__method
)


@add_from_json_method
@add_to_dict_method
@add__str__method
class Ingredient(db.Model):
    __tablename__ = "ingredient"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    displayname = db.Column(db.String(30), nullable=False)
    default_price = db.Column(db.Float(precision=2), nullable=False)
    quantity_per_unit = db.Column(db.Float(precision=2), nullable=False)
    is_spices = db.Column(db.Boolean, nullable=False)
    search_description = db.Column(db.String(75), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"), nullable=False)

    unit = db.relationship("Unit", backref="ingredient", lazy="select")

    @validates("name")
    def validate_name(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=4,
            max_length=50
        )
        return value

    @validates("displayname")
    def validate_displayname(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=3,
            max_length=30
        )
        return value

    @validates("default_price")
    def validate_default_price(self, key: str, value: Any) -> str:
        ModelValidator.validate_float(
            fieldname=key,
            value=value,
            min_=0.
        )
        return value

    @validates("quantity_per_unit")
    def validate_quantity_per_unit(self, key: str, value: Any) -> str:
        ModelValidator.validate_float(
            fieldname=key,
            value=value,
            min_=0.
        )
        return value

    @validates("is_spices")
    def validate_is_spices(self, key: str, value: bool) -> str:
        ModelValidator.validate_boolean(
            fieldname=key,
            value=value
        )
        return value

    @validates("search_description")
    def validate_search_description(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=4,
            max_length=75
        )
        return value

    @validates("unit_id")
    def validate_unit_id(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value
        )
        return value
