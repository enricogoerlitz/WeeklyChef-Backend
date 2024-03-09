from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.user.user import User
from server.core.models.api_models.user import user_model_public


class UserController(BaseCrudController):
    pass


user_controller = UserController(
    model=User,
    api_model=user_model_public,
    api_model_send=user_model_public,
    use_caching=False
)
