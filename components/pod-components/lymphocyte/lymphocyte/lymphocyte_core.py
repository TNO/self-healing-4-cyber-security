import logging
import time
from typing import Optional, Dict, List

import redis
from sh4cs_common.constants import get_lymphocite_registration_channel
from sh4cs_common.lazy_redis import LazyRedis

from anomaly_listener import AnomalyContainer, AnomalyContainerCollection
from docker_proxy import DockerProxy

logger = logging.getLogger()


class TTL:
    def __init__(self, time_to_live: int):
        self._ttl = time_to_live

    def reduce_by_half(self):
        if self._ttl > 0:
            self._ttl = self._ttl // 2

    def get_ttl(self) -> int:
        return self._ttl


def do_wait_before_next_action():
    logger.debug(f"Waiting for 5 seconds")
    time.sleep(5)


class LymphocyteContainer:
    def __init__(
        self,
        docker_proxy: DockerProxy,
        time_to_live: int,
        internal_anomaly_container_collection: AnomalyContainerCollection,
        external_anomaly_container_collection: AnomalyContainerCollection,
        lazy_redis: LazyRedis,
    ):
        self._docker_proxy = docker_proxy
        self._time_to_live = time_to_live
        self._internal_anomaly_container_collection = (
            internal_anomaly_container_collection
        )
        self._external_anomaly_container_collection = (
            external_anomaly_container_collection
        )
        self._lymphocytes: Dict[str, Lymphocyte] = {}
        self.__running = True
        self._lazy_redis = lazy_redis

    def __get_container_id_for_service_name(self, service_name: str) -> Optional[str]:
        try:
            return self._lazy_redis.get_redis().get(service_name)
        except redis.exceptions.ConnectionError as e:
            logger.warning(f"Error while connecting to redis: {e}")

        return None

    def __get_cell_for(self, container_id: str):
        if container_id in self._lymphocytes:
            return self._lymphocytes[container_id]

        internal_anomaly_container = (
            self._internal_anomaly_container_collection.get_container_for(container_id)
        )
        external_anomaly_container = (
            self._external_anomaly_container_collection.get_container_for(container_id)
        )

        lymphocyte = Lymphocyte(
            self._docker_proxy,
            container_id,
            self._time_to_live,
            internal_anomaly_container=internal_anomaly_container,
            external_anomaly_container=external_anomaly_container,
        )
        self._lymphocytes[container_id] = lymphocyte
        return lymphocyte

    def stop(self):
        self.__running = False

    def wait_for_docker_proxy(self):
        self._docker_proxy.proxy_health_check()

    def __execute_lymphocyte_algorithm(self, service_name: str):
        container_id_for_service = self.__get_container_id_for_service_name(
            service_name
        )
        if not container_id_for_service:
            logger.warning(
                f"No container id available for service name '{service_name}'"
            )
            return

        # TODO use the docker_proxy.get_name_for_container_id to standardize the names used.
        logger.debug(
            f"Found container id '{container_id_for_service}' for service '{service_name}'"
        )
        lymphocyte_cell = self.__get_cell_for(container_id_for_service)
        container_uptime = lymphocyte_cell.uptime_for_logging()

        logger.info(
            f"Container '{container_id_for_service}' had a remaining TTL of '{lymphocyte_cell.get_time_to_live()}'\t uptime={container_uptime}"
        )
        if not lymphocyte_cell.is_active():
            logger.warning(
                f"Current container id='{container_id_for_service}' but lymphocyte is no longer active"
            )
            self.__remove_cell(container_id_for_service)
            return

        if not lymphocyte_cell.container_exists():
            logger.debug(
                f"Container '{container_id_for_service}' no longer exists, exiting"
            )
            lymphocyte_cell.deactivate()
            return

        container_uptime = lymphocyte_cell.container_uptime()
        if not container_uptime:
            logger.warning(
                f"Uptime not available for container '{container_id_for_service}'"
            )
            return

        container_status = lymphocyte_cell.container_status()
        if not container_status:
            logger.warning(
                f"Container status not available for container '{container_id_for_service}'"
            )
            return

        if container_status != "running":
            logger.warning(
                f"Container status was not running, was '{container_status}'"
            )
            return

        if not lymphocyte_cell.should_kill():
            logger.debug(f"Nothing to do for container {container_id_for_service}")
            return

        logger.info(
            f"Determined container with id='{container_id_for_service}' should be killed!"
        )
        if not lymphocyte_cell.destroy_target_container():
            logger.error(
                f"Lymphocyte failed to kill/remove offending container '{container_id_for_service}'!!"
            )
        else:
            lymphocyte_cell.deactivate()

    def run(self):
        while self.__running:
            try:
                registered_services = self._get_services()
                logger.debug(
                    f"Found following services to manage: {registered_services}"
                )
                for service_name in registered_services:
                    self.__execute_lymphocyte_algorithm(service_name)
            except Exception as e:
                logger.exception(
                    f"Error while executing lymphocyte algorithm: {str(e)}"
                )
            finally:
                do_wait_before_next_action()

    def __remove_cell(self, current_container_id: str):
        del self._lymphocytes[current_container_id]
        self._internal_anomaly_container_collection.delete_container_for(
            current_container_id
        )
        self._external_anomaly_container_collection.delete_container_for(
            current_container_id
        )

    def _get_services(self) -> List[str]:
        lympho_channel = get_lymphocite_registration_channel()
        service_names = self._lazy_redis.get_redis().smembers(lympho_channel)
        return service_names


class Lymphocyte:
    def __init__(
        self,
        docker_proxy: DockerProxy,
        container_id: str,
        time_to_live: int,
        internal_anomaly_container: AnomalyContainer,
        external_anomaly_container: AnomalyContainer,
    ):
        self.__docker_proxy = docker_proxy
        self.__active = True
        self._ttl = TTL(time_to_live=time_to_live)
        self._container_id = container_id
        self._internal_anomaly_container = internal_anomaly_container
        self._external_anomaly_container = external_anomaly_container

    def is_active(self) -> bool:
        return self.__active

    def deactivate(self):
        self.__active = False

    def destroy_target_container(self) -> bool:
        kill_request = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="kill"
        )
        if not kill_request or not kill_request.ok:
            logger.warning(
                f"Failed to kill container, will not proceed to remove step for {self._container_id}"
            )
            return False

        remove_response = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="remove"
        )
        if not remove_response or not remove_response.ok:
            logger.warning(f"Unable to remove {self._container_id}")
            return False

        return remove_response.ok

    def pause_target_container(self) -> bool:
        response = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="pause"
        )
        if not response or not response.ok:
            logger.warning(f"Unable to pause {self._container_id}")
            return False

        return response.ok

    def remove_target_container(self) -> bool:
        response = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="remove"
        )
        if not response or not response.ok:
            logger.warning(f"Unable to remove {self._container_id}")
            return False

        return response.ok

    def stop_target_container(self) -> bool:
        response = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="stop"
        )
        if not response or not response.ok:
            logger.warning(f"Unable to stop {self._container_id}")
            return False

        return response.ok

    def container_exists(self) -> bool:
        response = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="exists"
        )
        if not response or not response.ok:
            logger.warning(
                f"Unable to retrieve whether container exists for {self._container_id}"
            )
            return False

        return response.ok

    def uptime_for_logging(self) -> str:
        container_uptime = self.container_uptime()
        if not container_uptime:
            return "unavailable"
        else:
            return str(container_uptime)

    def container_uptime(self) -> Optional[int]:
        response = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="uptime"
        )
        if not response or not response.ok:
            logger.warning(f"Unable to retrieve uptime for {self._container_id}")
            return None

        result = response.json()
        if "uptime" not in result:
            logger.warning(
                f"Response from HDDP had unexpected format, could not determine uptime for {self._container_id}"
            )
            return None

        return result["uptime"]

    def container_status(self) -> Optional[str]:
        response = self.__docker_proxy.send_docker_request(
            container_id=self._container_id, docker_action="status"
        )
        if not response or not response.ok:
            logger.warning(f"Unable to retrieve status for {self._container_id}")
            return None

        result = response.json()
        if "status" not in result:
            logger.warning(
                f"Response from HDDP had unexpected format, could not determine status for {self._container_id}"
            )
            return None

        return result["status"]

    def get_time_to_live(self) -> int:
        return self._ttl.get_ttl()

    def __uptime_is_above_ttl(self) -> bool:
        container_uptime = self.container_uptime()
        time_to_live = self.get_time_to_live()
        if container_uptime > time_to_live:
            logger.info(
                f"Container '{self._container_id}' violated TTL policy: uptime='{container_uptime}', TTL={time_to_live}"
            )
            return True
        return False

    def __has_internal_anomalies(self) -> bool:
        anomalies_for_lymphocyte = self._internal_anomaly_container.get_anomalies()
        if len(anomalies_for_lymphocyte) > 0:
            logger.info(
                f"Lymphocyte detected (internal) anomalies for container '{self._container_id}'!"
            )
            return True
        else:
            return False

    def __has_external_anomalies(self) -> bool:
        anomalies_for_lymphocyte = self._external_anomaly_container.get_anomalies()
        if len(anomalies_for_lymphocyte) > 0:
            logger.info(
                f"Lymphocyte detected (external) anomalies for container '{self._container_id}'!"
            )
            return True
        else:
            return False

    def reduce_ttl(self):
        ttl_before_change = self._ttl.get_ttl()
        self._ttl.reduce_by_half()
        logger.info(
            f"Reduced TTL of {self._container_id} from '{ttl_before_change}' to {self._ttl.get_ttl()}"
        )

    def should_kill(self) -> bool:
        kill_flags = []
        has_external = self.__has_external_anomalies()

        if has_external:
            self.reduce_ttl()
            self._external_anomaly_container.clear_anomalies()

        has_internal = self.__has_internal_anomalies()
        kill_flags.append(has_internal)

        if has_internal:
            self._internal_anomaly_container.clear_anomalies()

        kill_flags.append(self.__uptime_is_above_ttl())

        return any(kill_flags)
