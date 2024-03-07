from server.core.controller.crud_controller import BaseCrudController
from server.core.models.db_models.user.user import User
from server.core.models.api_models.user import user_model


user_controller = BaseCrudController(
    model=User,
    api_model=user_model,
    api_model_send=user_model,
    use_caching=False
)
