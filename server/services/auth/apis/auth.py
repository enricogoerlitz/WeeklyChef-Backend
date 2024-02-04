from flask import request
from flask_restx import Resource, Namespace

from core.models.api_models.utils import error_model
from services.auth.controller import auth_controller
from core.models.api_models.auth import (
    login_model_send,
    register_model_send,
    jwt_model
)


ns = Namespace(
    name="Authentication",
    description=__name__,
    path="/api/v1/auth"
)


@ns.route("/register")
class AuthRegisterAPI(Resource):

    @ns.expect(register_model_send)
    @ns.response(code=200, model=jwt_model, description="JSON Web Token")
    @ns.response(code=400, model=error_model, description="Wrong user input")
    @ns.response(code=409, model=error_model, description="User is alrready existing")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    def post(self):
        return auth_controller.handle_register(request.get_json())


@ns.route("/token")
class LoginAPI(Resource):

    @ns.expect(login_model_send)
    @ns.response(code=200, model=jwt_model, description="JSON Web Token")
    @ns.response(code=400, model=error_model, description="Wrong user input")
    @ns.response(code=401, model=error_model, description="Invalid user credentials")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    def post(self):
        return auth_controller.handle_login(request.get_json())


@ns.route("/token/refresh")
class LoginRefreshAPI(Resource):

    @ns.response(code=200, model=jwt_model, description="JSON Web Token")
    @ns.response(code=401, model=error_model, description="Valid Refreshtoken is missing")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    def post(self):
        return auth_controller.handle_refresh_token()
