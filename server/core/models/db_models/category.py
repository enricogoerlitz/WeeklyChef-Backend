from typing import Any

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
class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(strlen.L50), unique=True, nullable=False)

    @validates("name")
    def validate_name(self, _, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname="name",
            value=value,
            min_length=4,
            max_length=strlen.L50
        )
        return value
