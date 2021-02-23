import time
from typing import Dict

import redis

import logging

logger = logging.getLogger()


class LazyRedis:
    def __init__(self, host: str, port: int, **kwargs):
        self._host = host
        self._port = port
        self._redis_connection = None
        self.__other_args: Dict = kwargs

    def get_redis(self) -> redis.Redis:
        if not self._redis_connection:
            self._redis_connection = redis.Redis(
                host=self._host, port=self._port, **self.__other_args
            )
        return self._redis_connection

    def wait_for_redis(self) -> bool:
        while True:
            try:
                self.get_redis().ping()
                return True
            except (redis.exceptions.ConnectionError, ConnectionRefusedError) as e:
                logger.info("Waiting for redis to become available ")
                time.sleep(5)
            except Exception as e:
                return False
