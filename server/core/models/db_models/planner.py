"""

=> Keine Zeiten, sondern Positionen für ordering

Man kann mehrere Planner erstellen und andere leute einladen
"""

from typing import Any
from datetime import datetime
from dateutil import parser

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
class RecipePlanner(db.Model):
    __tablename__ = "rplanner"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    owner_user_id = db.Column(db.Integer, nullable=False)  # noqa
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    items = db.relationship("RecipePlannerItem", lazy="select")

    __table_args__ = (
        UniqueConstraint(
            "name",
            "owner_user_id",
            name="qu_rplanner_name_user_id"
        ),
    )

    @validates("name")
    def validate_name(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=1,
            max_length=25
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
    def validate_owner_is_active(self, key: str, value: Any) -> str:
        ModelValidator.validate_boolean(
            fieldname=key,
            value=value
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class RecipePlannerItem(db.Model):
    """
    Spaghetti Carbonara am 05.01.2024 an Stelle 5 und für 2 Personen
    Das Rezept darf nur einmal am Tag geplant werden

    get by rplanner_id und date_form
    """
    __tablename__ = "rplanner_item"

    id = db.Column(db.Integer,  primary_key=True)
    rplanner_id = db.Column(db.Integer, db.ForeignKey("rplanner.id"), nullable=False)  # noqa
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"), nullable=False)  # noqa
    date = db.Column(db.Date, nullable=False)
    label = db.Column(db.String(20), nullable=False, default="")
    order_number = db.Column(db.Integer, nullable=False)
    planned_recipe_person_count = db.Column(db.Integer, nullable=False)

    recipe = db.relationship("Recipe", lazy="select")

    # Unique together: rplanner_id, date, order_number

    @validates("rplanner_id")
    def validate_rplanner_id(self, key: str, value: Any) -> str:
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

    @validates("date")
    def validate_date(self, key: str, value: Any) -> str:
        ModelValidator.validate_datetime(
            fieldname=key,
            value=value
        )

        value: datetime = parser.parse(value)
        value = value.replace(hour=0, minute=0, second=0, microsecond=0).date()

        return value

    @validates("order_number")
    def validate_order_number(self, key: str, value: Any) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value,
            min_=1
        )
        return value

    @validates("planned_recipe_person_count")
    def validate_planned_recipe_person_count(
        self,
        key: str,
        value: Any
    ) -> str:
        ModelValidator.validate_integer(
            fieldname=key,
            value=value,
            min_=1
        )
        return value


@add_from_json_method
@add_to_dict_method
@add__str__method
class UserSharedRecipePlanner(db.Model):
    """
    Extra Route für planner/shared -> retuns list of Planner shared with me
    """
    __tablename__ = "rplanner_user"

    rplanner_id = db.Column(db.Integer, db.ForeignKey("rplanner.id"), primary_key=True)  # noqa
    user_id = db.Column(db.Integer, primary_key=True)  # noqa
    can_edit = db.Column(db.Boolean, nullable=False)

    planner = db.relationship("RecipePlanner", backref="rplanner_user", lazy="select")  # noqa

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
