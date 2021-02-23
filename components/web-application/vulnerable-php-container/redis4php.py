import logging
import os
import time

from sh4cs_common.constants import get_lymphocite_registration_channel
from sh4cs_common.lazy_redis import LazyRedis
from sh4cs_common.utils import get_container_name

REDIS_SERVER_PORT = int(os.environ.get("REDIS_SERVER_PORT", 6379))
REDIS_SERVER_HOST = os.environ.get("REDIS_SERVER_HOST", "redis")

logger = logging.getLogger()


def register_myself_in_redis_for_lymphocite(lazy_redis_instance: LazyRedis):
    container_name = get_container_name()
    logger.info(f"Registering container with name: '{container_name}'")
    label = "auth_php"

    lazy_redis_instance.get_redis().sadd(get_lymphocite_registration_channel(), label)
    lazy_redis_instance.get_redis().set(label, container_name)


def main():
    redis_instance = LazyRedis(host=REDIS_SERVER_HOST, port=REDIS_SERVER_PORT, db=0)
    while not redis_instance.wait_for_redis():
        time.sleep(1)
    register_myself_in_redis_for_lymphocite(redis_instance)


if __name__ == "__main__":
    main()
