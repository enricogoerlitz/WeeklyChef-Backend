from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.utils import decode_token

from server.core.permissions.general import IsAdminOrStaff
from server.services.auth.controller import auth_controller
from server.core.models.api_models.user import user_model
from server.core.models.api_models.auth import register_model_send
from server.core.models.api_models.utils import error_model
from server.services.auth.controller.user import user_controller


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
    def get(self):
        # TODO: ONLY USERNAMES!
        return user_controller.handle_get_list(
            reqargs=request.args
        )

    @ns.expect(register_model_send)
    @ns.response(code=200, model=None, description="List of user models")  # noqa
    @ns.response(code=400, model=error_model, description="Wrong user input")
    @ns.response(code=401, model=error_model, description="User unauthorized")  # noqa
    @ns.response(code=409, model=error_model, description="User is already existing")  # noqa
    @ns.response(code=500, model=error_model, description="Internal error message")  # noqa
    @jwt_required()
    @IsAdminOrStaff
    def post(self):
        # TODO: CHANGE ROUTE: /admin/user/ !!!
        data, status_code = auth_controller.handle_register(request.get_json())
        if status_code == 200:
            data = decode_token(data["access_token"]).get("sub")

        return data, status_code

    # TODO: patch for adding /admin/user/ removing roles etc


@ns.route("/me")
class UserMeAPI(Resource):

    @ns.response(code=200, model=user_model, description="Currently logged in user")  # noqa
    @ns.response(code=401, model=error_model, description="Token was expired")  # noqa
    @jwt_required()
    def get(self):
        return get_jwt_identity(), 200
