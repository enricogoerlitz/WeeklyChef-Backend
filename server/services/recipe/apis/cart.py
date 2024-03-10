from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from server.utils import jwt
from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.models.api_models.cart import (
    cart_item_model, cart_item_model_send,
    cart_model_detail, cart_model_send, user_shared_cart_model)
from server.services.recipe.controller.cart import (
    cart_controller, cart_item_controller,
    user_shared_cart_controller)
from server.core.permissions.cart import (
    IsCartOwner,
    IsCartOwnerOrCanEdit
)

ns = Namespace(
    name="Cart",
    description=__name__,
    path="/api/v1/cart"
)


@ns.route("/")
class CartListAPI(Resource):

    @ns.response(code=200, model=[cart_model_detail], description=sui.desc_list(ns.name))       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def get(self):
        return cart_controller.handle_get_list(
            reqargs=request.args,
            user_id=jwt.get_user_id()
        )

    @ns.expect(cart_model_send)
    @ns.response(code=201, model=cart_model_detail, description=sui.desc_added(ns.name))        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))           # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")              # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    def post(self):
        data = jwt.add_user_id_to_data(
            data=request.get_json(),
            fieldname="owner_user_id"
        )

        return cart_controller.handle_post(data)


@ns.route("/<int:id>")
class CartAPI(Resource):

    @ns.response(code=200, model=cart_model_detail, description=sui.desc_get(ns.name))          # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwnerOrCanEdit
    def get(self, id):
        return cart_controller.handle_get(id)

    @ns.expect(cart_model_send)
    @ns.response(code=200, model=cart_model_detail, description=sui.desc_update(ns.name))       # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwnerOrCanEdit
    def patch(self, id):
        return cart_controller.handle_patch(
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")              # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwner
    def delete(self, id):
        return cart_controller.handle_delete(id)


@ns.route("/<int:id>/clear")
class CartClearAPI(Resource):

    @ns.response(code=204, model=None, description=sui.desc_get(ns.name))                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))           # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwnerOrCanEdit
    def get(self, id):
        return cart_controller.handle_clear_cart(id)


@ns.route("/<int:id>/item")
class CartItemListAPI(Resource):

    @ns.expect(cart_item_model_send)
    @ns.response(code=201, model=cart_item_model, description=sui.desc_added("CartItem"))       # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("CartItem"))        # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")              # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwnerOrCanEdit
    def post(self, id):
        data = request.get_json()
        data["cart_id"] = id

        return cart_item_controller.handle_post(
            data=data
        )


@ns.route("/<int:id>/item/<int:item_id>")
class CartItemAPI(Resource):
    @ns.expect(cart_item_model_send)
    @ns.response(code=200, model=cart_item_model, description=sui.desc_update("CartItem"))      # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("CartItem"))        # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")              # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwnerOrCanEdit
    def patch(self, id, item_id):
        return cart_item_controller.handle_patch(
            id=item_id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("CartItem"))                 # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("CartItem"))        # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwnerOrCanEdit
    def delete(self, id, item_id):
        return cart_item_controller.handle_delete(item_id)


@ns.route("/<int:id>/access/edit/user/<int:user_id>")
class UserSharedRecipePlannerAPI(Resource):

    @ns.response(code=201, model=user_shared_cart_model, description=sui.desc_added("UserSharedCollection"))    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))                       # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("UserSharedCollection"))            # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                       # noqa
    @jwt_required()
    @IsCartOwner
    def post(self, id, user_id):
        data = {
            "cart_id": id,
            "user_id": user_id
        }

        return user_shared_cart_controller.handle_post(
            data=data,
            unique_primarykey=(id, user_id)
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("UserSharedRecipePlanner"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                       # noqa
    @jwt_required()
    @IsCartOwner
    def delete(self, id, user_id):
        return user_shared_cart_controller.handle_delete(id=(id, user_id))                      # noqa
