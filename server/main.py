""""""
from app import create_app
from api import api
from services.heathcheck.apis.heathcheck import ns as ns_heathcheck
from services.auth.apis.auth import ns as ns_auth


if __name__ == "__main__":
    app = create_app()

    api.add_namespace(ns_heathcheck)
    api.add_namespace(ns_auth)

    app.run(
        debug=True,
        threaded=True,
        port=8080
    )
