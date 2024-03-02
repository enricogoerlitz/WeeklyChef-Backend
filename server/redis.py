# type: ignore
import os
import json
import threading

from flask import request
from redis import Redis
from dotenv import load_dotenv

from server.db import db
from server.logger import logger


load_dotenv()


DEFAULT_CACHE_TIME = 60 * 60

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)


def gen_key(
        model: db.Model,
        path: str = None
) -> str:
    try:
        if path is None:
            path = request.full_path

        return f"{model.__name__}:{path}"
    except Exception as e:
        _log_redis_error(e)


def get(key: str) -> dict:
    try:
        obj = redis.get(key)
        if obj is None:
            return None

        return json.loads(obj)
    except Exception as e:
        _log_redis_error(e)
        return None


def set(
        key: str,
        value: dict,
        ex: int = DEFAULT_CACHE_TIME
) -> None:
    try:
        value = json.dumps(value)
        redis.set(key, value, ex=ex)
    except Exception as e:
        _log_redis_error(e)


def clear_cache(key_pattern: str) -> None:
    try:
        for key in redis.keys(key_pattern):
            redis.delete(key)
    except Exception as e:
        _log_redis_error(e)


def set_async(
        key: str,
        value: dict,
        ex: int = DEFAULT_CACHE_TIME
) -> threading.Thread:
    thread = threading.Thread(target=set, args=[key, value, ex])
    thread.start()
    return thread


def clear_cache_async(key_pattern: str) -> threading.Thread:
    thread = threading.Thread(target=clear_cache, args=[key_pattern])
    thread.start()
    return thread


def _log_redis_error(e: Exception) -> None:
    msg = f"Redis caching error: {str(e)}"
    logger.error(msg)
