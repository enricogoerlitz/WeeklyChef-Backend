import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] [%(levelname)s] %(filename)s %(message)s",
    datefmt="%d.%m.%Y %H:%M:%S,%f"
)

logger = logging.getLogger(__name__)
