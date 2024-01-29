""""""
from sqlalchemy import or_
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request


from db import db
from errors import errors
from core.models.api_models.auth import register_model_send
from core.models.db_models.user import User, Role
from core.utils import roles
from utils.jwt import JsonWebTokenDTO


def handle_register(req_data: dict) -> tuple[User, JsonWebTokenDTO]:
    """
    Adds an user to database, creates an JsonWebTokenDTO and returns
    the created User and JsonWebTokenDTO.

    Args:
        user (User): user to register

    Returns:
        tuple[User, JsonWebTokenDTO]: new user from db and JWT
    """
    user: User = User.from_json(req_data, register_model_send)

    _validate_user_is_existing(user)

    standard_role = Role.query.filter_by(name=roles.STANDARD).first()
    user.roles.append(standard_role)

    db.session.add(user)
    db.session.commit()

    return user, JsonWebTokenDTO.create(user.to_identity())


def handle_login(req_data: dict) -> tuple[User, JsonWebTokenDTO]:
    username = req_data.get("username", None)
    email = req_data.get("email", None)
    password = req_data.get("password", None)
    if (
        username is None and
        email is None
    ):
        raise errors.DbModelFieldRequieredException("username or email")

    filter_kwargs = {"username": username} \
        if username is not None else {"email": email}

    db_user: User = User.query.filter_by(**filter_kwargs).first()

    if db_user is None or not db_user.check_password(password):
        raise errors.InvalidLoginCredentialsException()

    return db_user, JsonWebTokenDTO.create(db_user.to_identity())


def handle_refresh_token() -> JsonWebTokenDTO:
    verify_jwt_in_request(refresh=True)
    jwt_identity = get_jwt_identity()
    return JsonWebTokenDTO.create(jwt_identity)


def _validate_user_is_existing(user: User) -> None:
    is_existing_count = User.query.filter(
        or_(
            User.email == user.email,
            User.username == user.username
        )
    ).count()

    if is_existing_count > 0:
        raise errors.UserAlreadyExistingException()
