"""
User Models
"""
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates

from db import db
from utils import model_validator
from utils.decorators import add_to_dict_method, add_from_json_method
from werkzeug.security import generate_password_hash, check_password_hash


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
    def validate_username(self, _, name: str) -> str:
        model_validator.validate_string(
            fieldname="name",
            value=name,
            min_length=1,
            max_length=50
        )
        return name


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
        self.email = email.lower()
        self.username = username
        self.set_password(password)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    @validates("email")
    def validate_email(self, _, email: str) -> str:
        model_validator.validate_email(
            fieldname="email",
            email=email,
            max_length=120
        )
        return email

    @validates("username")
    def validate_username(self, _, username: str) -> str:
        model_validator.validate_string(
            fieldname="username",
            value=username,
            min_length=5,
            max_length=50
        )
        return username

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
