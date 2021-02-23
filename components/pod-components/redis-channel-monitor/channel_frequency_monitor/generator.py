import os
import random
from time import sleep
import redis


def publish_events(redis_client: redis.Redis, amount: int):
    for counter in range(100):
        number = random.randint(0, 100)
        redis_client.publish(monitor_channel, number)
        print("event #", counter)


if __name__ == "__main__":

    redis_host = os.environ["REDIS_HOST"]
    monitor_channel = os.environ["REDIS_MONITOR_CHANNEL"]

    done = False

    while not done:
        try:
            redis_client = redis.Redis(host=redis_host)
            publish_events(redis_client=redis_client, amount=10000)
        except redis.exceptions.ConnectionError:
            done = False
            print("Connection refused, trying again...")
            sleep(2)
