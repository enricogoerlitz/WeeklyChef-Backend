""""""
from config import create_app
from api import api
from services.heathcheck.apis.heathcheck import ns as ns_heathcheck
from services.auth.apis.auth import ns as ns_auth
from services.auth.apis.user import ns as ns_user
from services.recipe.apis.recipe import ns as ns_recipe
from services.recipe.apis.ingredient import ns as ns_ingredient
from services.recipe.apis.category import ns as ns_category
from services.recipe.apis.unit import ns as ns_unit
from services.recipe.apis.tag import ns as ns_tag


if __name__ == "__main__":
    app = create_app()

    api.add_namespace(ns_heathcheck)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_user)
    api.add_namespace(ns_recipe)
    api.add_namespace(ns_ingredient)
    api.add_namespace(ns_category)
    api.add_namespace(ns_unit)
    api.add_namespace(ns_tag)

    app.run(
        debug=True,
        threaded=True,
        port=8080
    )
