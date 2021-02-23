import json
import logging
import os
import time

import redis
from sh4cs_common.constants import (
    get_auth_anomalies_channel,
    get_auth_failed_attempts_channel,
)
from sh4cs_common.lazy_redis import LazyRedis
from sh4cs_common.models import FailedLoginAttempt
from sh4cs_common.utils import setup_logging

from sliding_window import EventManager


def main():
    logger = setup_logging(
        package_name="channel_frequency_monitor",
        level=logging.getLevelName(logging.DEBUG),
    )
    redis_host = os.environ.get("REDIS_HOST", "redis")
    channel_to_monitor = get_auth_failed_attempts_channel()
    channel_to_output_on = get_auth_anomalies_channel()
    minute_frequency_threshold = int(os.environ.get("MINUTE_FREQUENCY_THRESHOLD", 10))

    lazy_redis = LazyRedis(host=redis_host, port=6379)
    redis_instance = lazy_redis.get_redis()

    logger.info(f"Starting authentication anomaly detector")
    logger.info(f"Connected to redis storage @ {redis_host}")

    event_manager = EventManager(minute_frequency_threshold=minute_frequency_threshold)

    connected = False
    subscription = None
    while not connected:
        try:
            subscription = redis_instance.pubsub(ignore_subscribe_messages=True)
            subscription.subscribe(channel_to_monitor)
            connected = True
        except redis.exceptions.ConnectionError:
            connected = False
            print("Redis not ready yet, trying again...")
            time.sleep(2)

    if not subscription:
        logger.error(f"Failed to create subscription on redis, exiting")
        raise RuntimeError(f"Failed to create subscription on redis, exiting")

    logger.info(f"Subscribed to following redis channel: '{channel_to_monitor}'")
    # We are expecting @FailedLoginAttempt as input
    for event in subscription.listen():
        if event["type"] != "message":
            continue

        event_data = event["data"]
        event_manager.add_event(FailedLoginAttempt(**json.loads(event_data)))
        possible_anomalies = event_manager.get_anomalies()
        if not possible_anomalies:
            continue

        for anomaly in possible_anomalies:
            logger.info(f"Found anomaly, publishing on '{channel_to_output_on}'")
            redis_instance.publish(channel_to_output_on, anomaly.to_redis())


if __name__ == "__main__":
    main()
