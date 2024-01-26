"""
/api/v1
        /register
        /token
        /token/refresh
"""
from flask import Blueprint, request

from errors import errors, http_errors
from logger import logger
from services.auth.controller import auth_controller


bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/v1/auth"
)


@bp.route("/register", methods=["POST"])
def register():
    try:
        added_user, jwt = auth_controller.handle_register(request.get_json())

        logger.info(f"User added: {added_user}")
        return jwt.to_dict()

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


@bp.route("/token", methods=["POST"])
def login():
    try:
        login_user, jwt = auth_controller.handle_login(request.get_json())

        logger.info(f"User login: {login_user}")
        return jwt.to_dict()
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


@bp.route("/token/refresh", methods=["POST"])
def refresh():
    try:
        jwt_refreshed = auth_controller.handle_refresh_token()
        return jwt_refreshed.to_dict()
    except Exception as e:
        logger.error(e)
        return http_errors.UNEXPECTED_ERROR_RESULT
