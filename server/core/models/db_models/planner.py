"""
Recipe planner models

=> Keine Zeiten, sondern Positionen für ordering

Man kann mehrere Planner erstellen und andere leute einladen
"""

from typing import Any

from sqlalchemy import UniqueConstraint
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
class RecipePlanner(db.Model):
    __tablename__ = "rplanner"

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
    rplanner_id = db.Column(db.Integer, db.ForeignKey("rplanner.id"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.id"))
    date = db.Column(db.Date, nullable=False)
    label = db.Column(db.String(20), nullable=False, default="")
    order_number = db.Column(db.Integer, nullable=False)
    planned_recipe_person_count = db.Column(db.Integer, nullable=False)

    recipe = db.relationship("Recipe", backref="rplanner_item", lazy="joined")

    __table_args__ = (
        UniqueConstraint(
            "rplanner_id",
            "date",
            "order_number",
            name="qu_rplanner_date_ordernum"
        ),
    )


@add_from_json_method
@add_to_dict_method
@add__str__method
class UserSharedRecipePlanner(db.Model):
    """
    Extra Route für planner/shared -> retuns list of Planner shared with me
    """
    __tablename__ = "rplanner_user"

    rplanner_id = db.Column(db.Integer, db.ForeignKey("rplanner.id"), primary_key=True)  # noqa
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # noqa
    can_edit = db.Column(db.Boolean, nullable=False)

    planner = db.relationship("RecipePlanner", backref="rplanner_user", lazy="select")  # noqa

    __table_args__ = (
        UniqueConstraint("rplanner_id", "user_id", name="uq_rplanner_user"),
    )
