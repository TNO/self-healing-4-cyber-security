import json
import logging
import threading
import time
from typing import List, Dict

import redis
from sh4cs_common.constants import get_auth_anomalies_channel
from sh4cs_common.lazy_redis import LazyRedis
from sh4cs_common.models import FailedLoginAnomaly, AnomalyModel

from mongo_puller import MongoPuller

logger = logging.getLogger()


class AnomalyContainer:
    def __init__(self):
        self._anomalies = []

    def add_anomaly(self, anomaly: AnomalyModel):
        logger.info(f"Anomaly detected: {anomaly}")
        self._anomalies.append(anomaly)

    def get_anomalies(self) -> List[AnomalyModel]:
        return self._anomalies

    def clear_anomalies(self):
        self._anomalies.clear()


class AnomalyContainerCollection:
    def __init__(self):
        self._anomaly_binding: Dict[str, AnomalyContainer] = {}

    def get_container_for(self, container_id: str) -> AnomalyContainer:
        if container_id in self._anomaly_binding:
            return self._anomaly_binding[container_id]

        for stored_container_id in self._anomaly_binding.keys():
            if (
                container_id in stored_container_id
                or stored_container_id in container_id
            ):
                logger.debug(
                    f"No exact match for anomaly container, found '{stored_container_id}' using id='{container_id}'"
                )
                return self._anomaly_binding[stored_container_id]

        anomaly_container = AnomalyContainer()
        self._anomaly_binding[container_id] = anomaly_container
        return anomaly_container

    def delete_container_for(self, current_container_id: str):
        del self._anomaly_binding[current_container_id]


class InternalAnomalyListener(threading.Thread):
    def __init__(
        self,
        lazy_redis: LazyRedis,
        anomaly_container_collection: AnomalyContainerCollection,
    ):
        threading.Thread.__init__(self)
        self._lazy_redis = lazy_redis
        self._anomaly_container_collection = anomaly_container_collection
        self.daemon = True

    def run(self):
        logger.info(f"Starting redis anomaly poller with daemon={self.daemon}")
        channel_to_subscribe_on = get_auth_anomalies_channel()
        try:
            connected = False
            subscription = None
            while not connected:
                try:
                    subscription = self._lazy_redis.get_redis().pubsub(
                        ignore_subscribe_messages=True
                    )
                    subscription.subscribe(channel_to_subscribe_on)
                    connected = True
                except redis.exceptions.ConnectionError:
                    connected = False
                    logger.debug("Redis not ready yet, trying again...")
                    time.sleep(2)

            if not subscription:
                logger.error(f"Failed to create subscription on redis, exiting")
                raise RuntimeError(f"Failed to create subscription on redis, exiting")

            logger.info(
                f"Subscribed to following redis channel: '{channel_to_subscribe_on}'"
            )
            # We are expecting @FailedLoginAnomaly as input
            for event in subscription.listen():
                if event["type"] != "message":
                    continue

                event_data = event["data"]
                detected_anomaly = FailedLoginAnomaly(**json.loads(event_data))
                anomaly_container = (
                    self._anomaly_container_collection.get_container_for(
                        container_id=detected_anomaly.get_affected_container()
                    )
                )
                anomaly_container.add_anomaly(detected_anomaly)
        except Exception as e:
            logger.exception(e)
        logger.info("Stopped redis anomaly poller")


class ExternalAnomalyListener(threading.Thread):
    def __init__(
        self,
        mongo_puller: MongoPuller,
        anomaly_container_collection: AnomalyContainerCollection,
    ):
        threading.Thread.__init__(self)
        self._mongo_puller = mongo_puller
        self._anomaly_container_collection = anomaly_container_collection
        self.daemon = True
        self.running = True  # setting the thread running to true

    def run(self):
        logger.info(f"Starting mongo anomaly poller with daemon={self.daemon}")
        while self.running:
            try:
                self._mongo_puller.connect()
                for detected_anomaly in self._mongo_puller.get_anomalies():
                    anomaly_container = (
                        self._anomaly_container_collection.get_container_for(
                            container_id=detected_anomaly.get_affected_container()
                        )
                    )
                    anomaly_container.add_anomaly(detected_anomaly)
            except Exception as e:
                logger.exception(e)
            finally:
                time.sleep(1)
        logger.info("Stopped mongo anomaly poller")
