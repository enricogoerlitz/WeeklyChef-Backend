"""

"""
from logger import logger
from flask import Blueprint


bp = Blueprint(
    "heathcheck",
    __name__,
    url_prefix="/api/v1"
)


@bp.route("/heathcheck")
def get():
    logger.info("heathcheck requested.")
    return {"heathcheck": "ok"}, 200
