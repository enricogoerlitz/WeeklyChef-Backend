"""
/api/v1
        /register
        /token
        /token/refresh
"""
from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended.exceptions import NoAuthorizationError

from errors import errors, http_errors
from logger import logger
from services.auth.controller import auth_controller
from core.models.api_models.auth import login_model, register_model, jwt_model
from core.models.api_models.utils import error_model


ns = Namespace(
    "Authentication",
    __name__,
    path="/api/v1/auth"
)


@ns.route("/register")
class AuthRegister(Resource):

    @ns.expect(register_model)
    @ns.response(code=200, model=jwt_model, description="JSON Web Token")
    @ns.response(code=400, model=error_model, description="Wrong user input")
    @ns.response(code=409, model=error_model, description="User is alrready existing")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    def post(self):
        try:
            added_user, jwt = auth_controller.handle_register(
                request.get_json())

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


@ns.route("/token")
class Login(Resource):

    @ns.response(code=200, model=jwt_model, description="JSON Web Token")
    @ns.response(code=400, model=error_model, description="Wrong user input")
    @ns.response(code=401, model=error_model, description="Invalid user credentials")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    def post(self):
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


@ns.route("/token/refresh")
class LoginRefresh(Resource):

    @ns.expect(login_model)
    @ns.response(code=200, model=jwt_model, description="JSON Web Token")
    @ns.response(code=401, model=error_model, description="Valid Refreshtoken is missing")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    def post(self):
        try:
            jwt_refreshed = auth_controller.handle_refresh_token()
            return jwt_refreshed.to_dict()
        except NoAuthorizationError as e:
            return http_errors.unauthorized(e)
        except Exception as e:
            logger.error(type(e))
            return http_errors.UNEXPECTED_ERROR_RESULT
