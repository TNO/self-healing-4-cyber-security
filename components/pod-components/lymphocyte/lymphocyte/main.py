"""
T Killer main script
1. get info about job container to watch
2. sends kill signal to docker-proxy api
"""
import logging
import os

from sh4cs_common.lazy_redis import LazyRedis
from sh4cs_common.utils import setup_logging

from anomaly_listener import (
    InternalAnomalyListener,
    AnomalyContainerCollection,
    ExternalAnomalyListener,
)
from docker_proxy import DockerProxy
from lymphocyte_core import LymphocyteContainer
from mongo_puller import MongoPuller

logger = setup_logging(
    package_name="lymphocyte", level=logging.getLevelName(logging.INFO)
)


def create_docker_proxy() -> DockerProxy:
    hddp_host = os.environ.get("HDDP_HOST", "172.17.0.1:80")

    return DockerProxy(hddp_host=hddp_host)


def create_redis_instance() -> LazyRedis:
    redis_server_host = os.environ.get("REDIS_SERVER_HOST", "redis")
    redis_server_port = int(os.environ.get("REDIS_SERVER_PORT", 6379))
    logger.info(f"Creating redis connection to {redis_server_host}:{redis_server_port}")
    redis_instance = LazyRedis(
        host=redis_server_host, port=redis_server_port, db=0, decode_responses=True
    )
    return redis_instance


def create_mongo_puller(docker_proxy: DockerProxy) -> MongoPuller:
    mongo_host = os.environ.get("MONGODB_HOST", "mongo")
    mongo_port = int(os.environ.get("MONGODB_PORT", 27017))
    logger.info(f"Creating mongo connection to {mongo_host}:{mongo_port}")
    mongo_puller = MongoPuller(mongo_host, mongo_port, docker_proxy=docker_proxy)
    return mongo_puller


def create_internal_anomaly_listener(
    redis_instance: LazyRedis, anomaly_container_collection: AnomalyContainerCollection
) -> InternalAnomalyListener:
    return InternalAnomalyListener(
        lazy_redis=redis_instance,
        anomaly_container_collection=anomaly_container_collection,
    )


def create_external_anomaly_listener(
    anomaly_container_collection: AnomalyContainerCollection, docker_proxy: DockerProxy
) -> ExternalAnomalyListener:
    mongo_puller = create_mongo_puller(docker_proxy=docker_proxy)

    return ExternalAnomalyListener(
        mongo_puller=mongo_puller,
        anomaly_container_collection=anomaly_container_collection,
    )


def create_lymphocyte_container(
    redis_instance: LazyRedis,
    internal_anomaly_container_collection: AnomalyContainerCollection,
    external_anomaly_container_collection: AnomalyContainerCollection,
    docker_proxy: DockerProxy,
) -> LymphocyteContainer:

    # Allow containers to live 10 minutes
    container_initial_ttl = int(os.environ.get("TTL", 600))
    return LymphocyteContainer(
        docker_proxy=docker_proxy,
        time_to_live=container_initial_ttl,
        internal_anomaly_container_collection=internal_anomaly_container_collection,
        external_anomaly_container_collection=external_anomaly_container_collection,
        lazy_redis=redis_instance,
    )


def main():
    # Connect to redis, both in lymphocite and in the auth bastion
    # In auth bastion, push the container name into some (shared) channel
    # In lymphocite register to this channel and retrieve all containers to monitor
    # Use this list in the while loop
    redis_instance = create_redis_instance()
    docker_proxy = create_docker_proxy()

    internal_anomaly_container_collection = AnomalyContainerCollection()
    internal_anomaly_listener = create_internal_anomaly_listener(
        redis_instance=redis_instance,
        anomaly_container_collection=internal_anomaly_container_collection,
    )

    external_anomaly_container_collection = AnomalyContainerCollection()
    external_anomaly_listener = create_external_anomaly_listener(
        anomaly_container_collection=external_anomaly_container_collection,
        docker_proxy=docker_proxy,
    )

    lympho_container = create_lymphocyte_container(
        docker_proxy=docker_proxy,
        redis_instance=redis_instance,
        internal_anomaly_container_collection=internal_anomaly_container_collection,
        external_anomaly_container_collection=external_anomaly_container_collection,
    )

    logger.info("Lymphocyte starting up")
    internal_anomaly_listener.start()
    external_anomaly_listener.start()
    lympho_container.wait_for_docker_proxy()

    lympho_container.run()
    logger.info("Lymphocyte finished, closing application")
    lympho_container.stop()

    internal_anomaly_listener.join()

    external_anomaly_listener.running = False
    external_anomaly_listener.join()


if __name__ == "__main__":
    main()
