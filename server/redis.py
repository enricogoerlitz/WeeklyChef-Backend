import os

from redis import Redis
from dotenv import load_dotenv


load_dotenv()


DEFAULT_CACHE_TIME = 60 * 60

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

redis = Redis(host=REDIS_HOST, port="6379")
