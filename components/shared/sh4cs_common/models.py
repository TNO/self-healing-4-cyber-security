import abc
import json
from typing import Dict


class RedisModel(abc.ABC):
    def __init__(self, timestamp_epoch: int, affected_container: str):
        self._timestamp_epoch = timestamp_epoch
        self._affected_container = affected_container

    def get_timestamp_epoch(self) -> int:
        return self._timestamp_epoch

    def get_affected_container(self) -> str:
        return self._affected_container

    @abc.abstractmethod
    def to_dict(self):
        pass

    def to_redis(self) -> str:
        return json.dumps(self.to_dict())

    def __repr__(self):
        return f"{type(self)}: {self.to_dict()}"


class AnomalyModel(RedisModel, abc.ABC):
    pass


class FalcoAlert(AnomalyModel):
    def to_dict(self) -> Dict:
        return {
            "timestamp_epoch": self.get_timestamp_epoch(),
            "affected_container": self.get_affected_container(),
        }


class FailedLoginAnomaly(AnomalyModel):
    def __init__(self, timestamp_epoch: int, username: str, affected_container: str):
        """
        Model to serialize/deserialize through redis
        :param timestamp_epoch: Timestamp on which anomaly was established
        :param username: Username of account where anomaly originated for
        :param affected_container: Container name/identifier where anomaly originated from
        """
        super().__init__(timestamp_epoch, affected_container)
        self._detection_timestamp = timestamp_epoch
        self._username = username

    def get_username(self):
        return self._username

    def to_dict(self) -> Dict:
        return {
            "username": self.get_username(),
            "timestamp_epoch": self.get_timestamp_epoch(),
            "affected_container": self.get_affected_container(),
        }


class FailedLoginAttempt(RedisModel):
    def __init__(self, timestamp_epoch: int, username: str, affected_container: str):
        """
        Model to serialize/deserialize through redis
        :param timestamp_epoch: Timestamp on which login attempt was recorded
        :param username: Username of account where attempt originated for
        """
        super().__init__(timestamp_epoch, affected_container)
        self._username = username

    def get_username(self):
        return self._username

    def to_dict(self) -> Dict:
        return {
            "username": self.get_username(),
            "timestamp_epoch": self.get_timestamp_epoch(),
            "affected_container": self.get_affected_container(),
        }
