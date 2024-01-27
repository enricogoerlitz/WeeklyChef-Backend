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

from flask import request
from flask_restx import Resource, Namespace, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity

from logger import logger
from errors import errors, http_errors
from utils.jwt import userrole_required
from utils import roles
from services.auth.controller import auth_controller
from core.models.db_models.user import User
from core.models.api_models.user import user_model
from core.models.api_models.auth import register_model_send
from core.models.api_models.utils import error_model


ns = Namespace(
    name="User",
    description=__name__,
    path="/api/v1/user"
)


@ns.route("/")
class UserListAPI(Resource):

    @ns.response(code=200, model=[user_model], description="List of user models")  # noqa
    @ns.response(code=401, model=error_model, description="User unauthorized")  # noqa
    @ns.response(code=500, model=error_model, description="List of user models")  # noqa
    @jwt_required()
    @userrole_required([roles.ADMIN, roles.STAFF])
    def get(self):
        try:
            return marshal(User.query.all(), user_model)
        except Exception as e:
            logger.error(e)
            return http_errors.UNEXPECTED_ERROR_RESULT

    @ns.expect(register_model_send)
    @ns.response(code=200, model={}, description="List of user models")  # noqa
    @ns.response(code=400, model=error_model, description="Wrong user input")
    @ns.response(code=401, model=error_model, description="User unauthorized")  # noqa
    @ns.response(code=409, model=error_model, description="User is already existing")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    @jwt_required()
    @userrole_required([roles.ADMIN, roles.STAFF])
    def post(self):
        try:
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


@ns.route("/me")
class UserMeAPI(Resource):

    @ns.response(code=200, model=user_model, description="Currently logged in user")  # noqa
    @ns.response(code=401, model=error_model, description="Token was expired")  # noqa
    @jwt_required()
    def get(self):
        return get_jwt_identity()
