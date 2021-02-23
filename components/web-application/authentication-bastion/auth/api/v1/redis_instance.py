import os

from sh4cs_common.lazy_redis import LazyRedis

REDIS_SERVER_HOST = os.environ.get("REDIS_SERVER_HOST", "redis")
REDIS_SERVER_PORT = int(os.environ.get("REDIS_SERVER_PORT", 6379))

redis_instance = LazyRedis(host=REDIS_SERVER_HOST, port=REDIS_SERVER_PORT, db=0)
