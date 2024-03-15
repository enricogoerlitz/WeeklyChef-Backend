from typing import Any

from sqlalchemy.orm import validates

from server.db import db
from server.core.utils import model_validator as ModelValidator
from server.utils.decorators import add_to_dict_method


@add_to_dict_method
class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return str(self.to_dict())

    @validates("name")
    def validate_username(self, key, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=1,
            max_length=50
        )
        return value
