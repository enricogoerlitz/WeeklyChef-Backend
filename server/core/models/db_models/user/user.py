from typing import Any

from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from db import db
from core.utils import model_validator as ModelValidator
from utils.decorators import add_to_dict_method, add_from_json_method
from werkzeug.security import generate_password_hash, check_password_hash


@add_from_json_method
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    roles = db.relationship(
        "Role",
        secondary="user_roles",
        backref=db.backref("users", lazy="dynamic")
    )

    def __init__(self, email: str, username: str, password: str):
        self.email = email
        self.username = username
        self.validate_password("password", password)
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    @validates("email")
    def validate_email(self, key: str, value: str) -> str:
        ModelValidator.validate_email(
            fieldname=key,
            email=value,
            max_length=120
        )
        return value.lower()

    @validates("username")
    def validate_username(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=5,
            max_length=50
        )
        return value

    @validates("password")
    def validate_password(self, key: str, value: Any) -> str:
        ModelValidator.validate_string(
            fieldname=key,
            value=value,
            min_length=5,
            max_length=500
        )
        return value

    def to_identity(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "roles": [role.name for role in self.roles]
        }

    def __str__(self) -> str:
        return str(self.to_identity())


@add_from_json_method
@add_to_dict_method
class UserRoleComposite(db.Model):
    __tablename__ = "user_roles"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)  # noqa
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), primary_key=True)  # noqa

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )
