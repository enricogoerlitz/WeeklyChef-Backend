""""""
from flask import Response
from sqlalchemy import or_
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError


from db import db
from logger import logger
from errors import errors, http_errors
from core.models.api_models.auth import register_model_send
from core.models.db_models.user import User, Role
from core.enums import roles
from utils.jwt import JsonWebTokenDTO


def handle_register(user_data: dict) -> Response:
    """
    Adds an user to database, creates an JsonWebTokenDTO and returns
    the created User and JsonWebTokenDTO.

    Args:
        user (User): user to register

    Returns:
        tuple[User, JsonWebTokenDTO]: new user from db and JWT
    """

    try:
        user: User = User.from_json(user_data, register_model_send)

        _validate_user_is_existing(user)

        standard_role = Role.query.filter_by(name=roles.STANDARD).first()
        user.roles.append(standard_role)

        db.session.add(user)
        db.session.commit()

        jwt = JsonWebTokenDTO.create(user.to_identity())

        logger.info(f"User added: {user.to_identity()}")
        return jwt.to_dict(), 200

    except (errors.DbModelValidationException,
            errors.DbModelSerializationException) as e:
        logger.info(e)
        return http_errors.bad_request(e)

    except errors.UserAlreadyExistingException as e:
        logger.info(e)
        return http_errors.conflict(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_login(user_data: dict) -> tuple[User, JsonWebTokenDTO]:
    try:
        username = user_data.get("username", None)
        email = user_data.get("email", None)
        password = user_data.get("password", None)
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

        jwt = JsonWebTokenDTO.create(db_user.to_identity())

        logger.info(f"User login: {db_user.to_identity()}")
        return jwt.to_dict(), 200

    except (errors.DbModelValidationException,
            errors.DbModelSerializationException) as e:
        logger.info(e)
        return http_errors.bad_request(e)

    except errors.InvalidLoginCredentialsException as e:
        logger.info(e)
        return http_errors.unauthorized(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def handle_refresh_token() -> JsonWebTokenDTO:
    try:
        verify_jwt_in_request(refresh=True)
        jwt_identity = get_jwt_identity()
        return JsonWebTokenDTO.create(jwt_identity).to_dict()

    except NoAuthorizationError as e:
        return http_errors.unauthorized(e)

    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT


def _validate_user_is_existing(user: User) -> None:
    is_existing_count = User.query.filter(
        or_(
            User.email == user.email,
            User.username == user.username
        )
    ).count()

    if is_existing_count > 0:
        raise errors.UserAlreadyExistingException()
