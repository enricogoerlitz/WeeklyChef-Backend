from flask_restx import Resource, Namespace
from logger import logger


ns = Namespace(
    "Heathcheck",
    __name__,
    path="/api/v1"
)


@ns.route("/heathcheck")
class Heathcheck(Resource):

    def get(self):
        logger.info("heathcheck requested.")
        return {"heathcheck": "ok"}, 200
