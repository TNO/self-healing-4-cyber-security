import logging
import time
from typing import Optional

import requests

logger = logging.getLogger()


class DockerProxy:
    def __init__(self, hddp_host: str):
        self.__docker_proxy_endpoint = "http://" + hddp_host + "/api/v1"

    def send_docker_request(
        self, docker_action: str, container_id: str
    ) -> Optional[requests.Response]:
        data = {"container_identifier": container_id}
        try:
            response = requests.post(
                self.__docker_proxy_endpoint + "/docker/" + docker_action, data=data
            )
            if response.ok:
                logger.debug(
                    f"'{docker_action}' on container '{container_id}' SUCCESS: <{response.status_code}>\tcontent={response.content}"
                )
            else:
                logger.debug(
                    f"'{docker_action}' on container '{container_id}' FAILURE: <{response.status_code}>\tcontent={response.content}"
                )
            return response
        except requests.exceptions.RequestException:
            return None

    def proxy_health_check(self):
        logger.info(
            f"Waiting to establish connection to docker daemon proxy at location: '{self.__docker_proxy_endpoint}'"
        )
        while True:
            try:
                requests.get(self.__docker_proxy_endpoint)
                logger.info(
                    f"Connected to Docker Daemon proxy at location: '{self.__docker_proxy_endpoint}'"
                )
                return
            except requests.exceptions.ConnectionError:
                logger.debug(
                    "Could not reach Docker Daemon proxy, retrying in 2 seconds..."
                )
                time.sleep(2)

    def get_name_for_container_id(self, container_id: str) -> str:
        response = self.send_docker_request(
            docker_action="name", container_id=container_id
        )
        if not response or not response.ok:
            logger.warning(f"Unable to retrieve name for {container_id}")
            return container_id

        result = response.json()
        if "name" not in result:
            logger.error(
                f"Response from HDDP had unexpected format, could not determine name for {container_id}"
            )
            return container_id

        return result["name"]
