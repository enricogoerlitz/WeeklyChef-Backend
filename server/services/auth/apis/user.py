"""
/api/v1
        /user
        /role

        /role/<role_id>
        /role?id=1,2,3,4

        /user/<user_id>
        /user?id=1,2,3,4
        /user/<user_id>/role/<role_id>
"""
from flask import Blueprint, request

from services.auth.controller import auth_controller
from errors import errors, http_errors
from logger import logger
from core.models.db_models.user import User


bp = Blueprint(
    "user",
    __name__,
    url_prefix="/api/v1/user"
)


@bp.route("/", methods=["GET", "POST"])
def user():
    try:

        match request.method:
            case "GET":
                users: list[User] = User.query.all()
                return [user.to_identity() for user in users]
            case "POST":
                _, _ = auth_controller.handle_register(request.get_json())
                return {}, 201

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
