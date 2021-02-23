import datetime
import logging
import os

import dateutil.parser
import docker
import pytz
from docker import errors
from docker.models.containers import ContainerCollection, Container

if "DOCKER_HOST" not in os.environ:
    raise RuntimeError("DOCKER_HOST variable is not set!")

# TODO integrate ENTRYPOINT that injects IP https://stackoverflow.com/questions/48546124/what-is-linux-equivalent-of-host-docker-internal
DOCKER_HOST = os.environ["DOCKER_HOST"]

logger = logging.getLogger(__name__)


class DockerConnectionProxy:
    def __init__(self):
        self._docker_conn = None

    def _get_docker_connection(self):
        if not self._docker_conn:
            self._docker_conn = docker.from_env(
                environment={"DOCKER_HOST": DOCKER_HOST}
            )
        return self._docker_conn

    def _get_containers(self) -> ContainerCollection:
        return self._get_docker_connection().containers

    def find_container(self, container_name: str) -> Container:
        """
        :param container_name:
        :raises docker.errors.NotFound in case container is not found
        :raises docker.errors.APIError i
        :return:
        """
        containers = self._get_containers()
        try:
            return containers.get(container_name)
        except errors.NotFound as e:
            for container in containers.list():
                if container_name in container.name:
                    return container

            raise e


def parse_docker_started_at_time(started_at_string: str) -> datetime.datetime:
    return dateutil.parser.isoparse(started_at_string).replace(tzinfo=pytz.utc)


def is_container_running(container: Container) -> bool:
    current_container_status = container_status(container)
    logger.debug(
        f"Status for container {container.name} was {current_container_status}"
    )
    return current_container_status == "running"


def container_status(container: Container) -> str:
    return container.status


docker_connection_proxy: DockerConnectionProxy = DockerConnectionProxy()
