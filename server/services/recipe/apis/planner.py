from flask import request
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

from server.utils import jwt
from server.utils import swagger as sui
from server.core.models.api_models.utils import error_model
from server.core.models.api_models.planner import (
    qpp_recipe_planner_item_model,
    qpp_recipe_planner_model, recipe_planner_item_model,
    recipe_planner_item_model_send,
    recipe_planner_model, recipe_planner_model_detail,
    recipe_planner_model_send,
    user_shared_recipe_planner_model, user_shared_recipe_planner_model_send)
from server.services.recipe.controller.planner import (
    recipe_planner_controller,
    recipe_planner_item_controller, user_shared_recipe_planner_controller
)
from server.core.permissions.planner import (
    IsRecipePlannerOwner,
    IsRecipePlannerOwnerOrCanEdit,
    IsRecipePlannerOwnerOrHasAccess
)


ns = Namespace(
    name="Planner",
    description=__name__,
    path="/api/v1/planner"
)


@ns.route("/")
class RecipePlannerListAPI(Resource):

    @ns.expect(qpp_recipe_planner_model)
    @ns.response(code=200, model=[recipe_planner_model_detail], description=sui.desc_list(ns.name)) # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    def get(self):
        return recipe_planner_controller.handle_get_list(
            reqargs=request.args,
            user_id=jwt.get_user_id(),
            api_response_model=recipe_planner_model
        )

    @ns.expect(recipe_planner_model_send)
    @ns.response(code=201, model=recipe_planner_model_detail, description=sui.desc_added(ns.name))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict(ns.name))               # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                  # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    def post(self):
        data = jwt.add_user_id_to_data(
            data=request.get_json(),
            fieldname="owner_user_id"
        )

        return recipe_planner_controller.handle_post(data)


@ns.route("/<int:id>")
class RecipePlannerAPI(Resource):

    @ns.response(code=200, model=recipe_planner_model_detail, description=sui.desc_get(ns.name))    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))               # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsRecipePlannerOwnerOrHasAccess
    def get(self, id):
        return recipe_planner_controller.handle_get(id)

    @ns.expect(recipe_planner_model_send)
    @ns.response(code=200, model=recipe_planner_model_detail, description=sui.desc_update(ns.name)) # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))               # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                  # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsRecipePlannerOwnerOrCanEdit
    def patch(self, id):
        return recipe_planner_controller.handle_patch(
            id=id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete(ns.name))                        # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                           # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                          # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound(ns.name))               # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                           # noqa
    @jwt_required()
    @IsRecipePlannerOwner
    def delete(self, id):
        return recipe_planner_controller.handle_delete(id)


@ns.route("/<int:id>/item")
class RecipePlannerItemListAPI(Resource):

    @ns.expect(qpp_recipe_planner_item_model)
    @ns.response(code=200, model=[recipe_planner_item_model], description=sui.desc_list("RecipePlannerItem"))   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                       # noqa
    @jwt_required()
    @IsRecipePlannerOwnerOrHasAccess
    def get(self, id):
        return recipe_planner_item_controller.handle_get_list(
            reqargs=request.args,
            planner_id=id
        )

    @ns.expect(recipe_planner_item_model_send)
    @ns.response(code=201, model=recipe_planner_item_model, description=sui.desc_added("RecipePlannerItem"))    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))                       # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("RecipePlannerItem"))               # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                              # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                       # noqa
    @jwt_required()
    @IsRecipePlannerOwnerOrCanEdit
    def post(self, id):
        data = request.get_json()
        data["rplanner_id"] = id

        return recipe_planner_item_controller.handle_post(data)


@ns.route("/<int:id>/item/<int:item_id>")
class RecipePlannerItemAPI(Resource):
    @ns.expect(recipe_planner_item_model_send)
    @ns.response(code=200, model=recipe_planner_item_model, description=sui.desc_update("RecipePlannerItem"))   # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                      # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("RecipePlannerItem"))               # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                              # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                       # noqa
    @jwt_required()
    @IsRecipePlannerOwnerOrCanEdit
    def patch(self, id, item_id):
        return recipe_planner_item_controller.handle_patch(
            id=item_id,
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("RecipePlannerItem"))                # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                               # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                              # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("RecipePlannerItem"))       # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                               # noqa
    @jwt_required()
    @IsRecipePlannerOwnerOrCanEdit
    def delete(self, id, item_id):
        return recipe_planner_item_controller.handle_delete(item_id)


@ns.route("/<int:id>/item/<int:item_id>/reorder/<int:new_order_number>")
class RecipePlannerChangeOrderAPI(Resource):

    @ns.response(code=201, model=recipe_planner_item_model, description=sui.desc_added("RecipePlannerItem"))    # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                       # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                      # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                       # noqa
    @jwt_required()
    @IsRecipePlannerOwnerOrCanEdit
    def patch(self, id, item_id, new_order_number):
        return recipe_planner_item_controller.handle_post_change_order(
            id=item_id,
            new_order_number=new_order_number
        )


@ns.route("/<int:id>/access/user/<int:user_id>")
class UserSharedRecipePlannerAPI(Resource):

    @ns.expect(user_shared_recipe_planner_model_send)
    @ns.response(code=201, model=user_shared_recipe_planner_model, description=sui.desc_added("UserSharedRecipePlanner"))   # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))                                   # noqa
    @ns.response(code=409, model=error_model, description=sui.desc_conflict("UserSharedRecipePlanner"))                     # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                                   # noqa
    @jwt_required()
    @IsRecipePlannerOwner
    def post(self, id, user_id):
        data = {
            "rplanner_id": id,
            "user_id": user_id,
            "can_edit": request.get_json().get("can_edit")
        }

        return user_shared_recipe_planner_controller.handle_post(
            data=data,
            unique_primarykey=(id, user_id)
        )

    @ns.expect(user_shared_recipe_planner_model_send)
    @ns.response(code=200, model=user_shared_recipe_planner_model, description=sui.desc_update("UserSharedRecipePlanner"))  # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                                                   # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                                                  # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("UserSharedRecipePlanner"))                     # noqa
    @ns.response(code=415, model=error_model, description="Unsupported Mediatype")                                          # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                                                   # noqa
    @jwt_required()
    @IsRecipePlannerOwner
    def patch(self, id, user_id):
        return user_shared_recipe_planner_controller.handle_patch(
            id=(id, user_id),
            data=request.get_json()
        )

    @ns.response(code=204, model=None, description=sui.desc_delete("UserSharedRecipePlanner"))          # noqa
    @ns.response(code=400, model=error_model, description=sui.DESC_INVUI)                               # noqa
    @ns.response(code=401, model=error_model, description=sui.DESC_UNAUTH)                              # noqa
    @ns.response(code=404, model=error_model, description=sui.desc_notfound("Ressource"))               # noqa
    @ns.response(code=500, model=error_model, description=sui.DESC_UNEXP)                               # noqa
    @jwt_required()
    @IsRecipePlannerOwner
    def delete(self, id, user_id):
        return user_shared_recipe_planner_controller.handle_delete(id=(id, user_id))                    # noqa
