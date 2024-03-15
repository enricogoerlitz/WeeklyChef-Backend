# type: ignore
import os
import json

from typing import Any

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


class BaseRedisCaching:

    def gen_key(
            self,
            key: str,
            redis_addition_key: str = None
    ) -> str:
        try:
            if redis_addition_key is not None:
                key += f"/add-key={redis_addition_key}"

            return key
        except Exception as e:
            self._log_redis_error(e)

    def get(self, key: str) -> dict:
        try:
            obj = redis.get(key)
            if obj is None:
                return None

            return json.loads(obj)
        except Exception as e:
            self._log_redis_error(e)
            return None

    def set(
            self,
            key: str,
            value: dict,
            ex: int = DEFAULT_CACHE_TIME
    ) -> None:
        try:
            value = json.dumps(value)
            redis.set(key, value, ex=ex)
        except Exception as e:
            self._log_redis_error(e)

    def clear_cache(self, key_pattern: str) -> None:
        try:
            for key in redis.keys(key_pattern):
                redis.delete(key)
        except Exception as e:
            self._log_redis_error(e)

    def _log_redis_error(self, e: Exception) -> None:
        msg = f"Redis caching error: {str(e)}"
        logger.error(msg)


class ApiModelCache(BaseRedisCaching):

    def __init__(self, expiring_time: int) -> None:
        super().__init__()
        self._ex = expiring_time

    def gen_key(
            self,
            model: db.Model,
            path: str = None,
            redis_addition_key: str = None
    ) -> str:
        try:
            if path is None:
                path = request.full_path

            key = f"{model.__name__}:{path}"
            return super().gen_key(key, redis_addition_key)

        except Exception as e:
            self._log_redis_error(e)

    def set(self, key: str, value: dict) -> None:
        return super().set(key, value, self._ex)


class ApiAccessCache(BaseRedisCaching):

    def __init__(
            self,
            prefix: str,
            expiring_time: int = 60 * 5
    ) -> None:
        super().__init__()
        self._prefix = prefix
        self._ex = expiring_time

    def gen_key(
            self,
            model: db.Model,
            id: Any
    ) -> str:
        try:
            key = f"{self._prefix}:{model.__name__}:{str(id)}"
            return key
        except Exception as e:
            self._log_redis_error(e)

    def set(self, key: str) -> None:
        return super().set(key, {"access": True}, self._ex)

    def has_access(self, key: str) -> bool:
        cache_result = self.get(key)
        return (
            cache_result is not None and
            cache_result.get("access", False)
        )


api_cache: ApiModelCache = ApiModelCache(DEFAULT_CACHE_TIME)
