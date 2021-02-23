import logging
import re
from typing import Optional, List, Dict

import pymongo
from dateutil import parser
from sh4cs_common.models import FalcoAlert, AnomalyModel

from docker_proxy import DockerProxy

logger = logging.getLogger()

FALCO_PROGRAM = "falco"
SRPIO_PROGRAM = "srpio"


class FalcoMessage:
    def __init__(
        self, sm_date, sm_msg, sm_dtls, container_id_from_security_message: str
    ):
        self.__container_id_from_security_message = container_id_from_security_message
        self.__sm_dtls = sm_dtls.strip()
        self.__sm_msg = sm_msg.strip()
        # TODO fix regex so it does not include the trailing :
        self.__sm_date = sm_date[:-1]
        self.__epoch = self.__parse_date_to_epoch()

    def get_timestamp(self) -> str:
        return self.__sm_date

    def __parse_date_to_epoch(self) -> int:
        return parser.parse(self.__sm_date).timestamp()

    def get_message(self) -> str:
        return self.__sm_msg

    def get_details(self) -> str:
        return self.__sm_dtls

    def container_id(self) -> str:
        return self.__container_id_from_security_message

    def get_reporting_time_as_epoch(self) -> int:
        return self.__epoch


class FalcoMessageParser:
    @staticmethod
    def parse(sample: Dict) -> Optional[FalcoMessage]:
        """
        Below is the message we want to capture
        'MESSAGE': '2020-11-19T13:54:03.088739382+0000: Error File created below /dev by untrusted program (user=root user_loginuid=-1 command=touch /dev/file file=/dev/file container_id=23485e8f5f0f image=<NA>)'

        However some message look like this.. THANKS FALCO FOR A COMPLETELY DIFFERENT FORMAT
        'MESSAGE': '14:50:04.398938252: Critical Falco internal: syscall event drop. 1 system calls dropped in last second. (ebpf_enabled=1 n_drops=1 n_drops_buffer=1 n_drops_bug=0 n_drops_pf=0 n_evts=24881)'

        """
        searchme = sample["MESSAGE"]
        securitymsg = re.search(
            "([0-9]{1,4}-[0-9]{1,2}-[0-9]{1,2}[^:]*:[^:]*:[^:]*:)(.*)\((.*)(container_id=)([^\s]+)",
            searchme,
        )
        if not securitymsg:
            logging.debug(
                f"Message with id={sample['_id']} from falco recieved but not a security alert "
            )
            return None

        sm_date = securitymsg.group(1)
        sm_msg = securitymsg.group(2)
        sm_dtls = securitymsg.group(3)
        container_id_from_security_message = securitymsg.group(5)
        return FalcoMessage(
            sm_date, sm_msg, sm_dtls, container_id_from_security_message
        )


class MongoPuller:
    def __init__(
        self,
        host: str,
        port: int,
        docker_proxy: DockerProxy,
        database="detectors",
        collection="messages",
    ):
        self._docker_proxy = docker_proxy
        # connect to mongodb and list db names
        self.__database_host = host
        self.__database_port = port
        self.__database_name = database
        self.__collection_name = collection
        self.__mongo_client = None
        self.__database: Optional = None
        self.__message_collection: Optional = None
        self.__falco_message_parser = FalcoMessageParser()

    def connect(self):
        self._get_collection()

    def _get_collection(self) -> pymongo.collection.Collection:
        if not self.__mongo_client:
            self.__mongo_client = pymongo.MongoClient(
                self.__database_host, self.__database_port
            )
            logger.debug(
                f"Found following names in database: {self.__mongo_client.list_database_names()}"
            )

        if not self.__database:
            self.__database = self.__mongo_client[self.__database_name]

        if not self.__message_collection:
            self.__message_collection = self.__database[self.__collection_name]

        return self.__message_collection

    def __get_unprocessed_samples(self):
        """
        Get unprocessed rows oldest first where program is falco or srpio
        """
        return (
            self._get_collection()
            .find(
                {
                    "$and": [
                        {"PROCESSED": {"$exists": False}},
                        {"PROGRAM": {"$in": [FALCO_PROGRAM, SRPIO_PROGRAM]}},
                    ]
                }
            )
            .sort("DATE", -1)
            .limit(10)
        )

    def __get_name_for_container_id(self, container_id: str) -> str:
        return self._docker_proxy.get_name_for_container_id(container_id)

    def __handle_falco_entry(self, sample) -> Optional[FalcoAlert]:
        self._get_collection().update_one(
            {"_id": sample["_id"]}, {"$set": {"PROCESSED": "True"}}
        )

        falco_message = self.__falco_message_parser.parse(sample)
        if not falco_message:
            return None

        container_name = self.__get_name_for_container_id(falco_message.container_id())
        logger.debug(
            f"Found container name='{container_name}' for id='{falco_message.container_id()}' from falco"
        )
        return FalcoAlert(falco_message.get_reporting_time_as_epoch(), container_name)

    def get_anomalies(self) -> List[AnomalyModel]:
        anomalies = []
        try:
            for sample in self.__get_unprocessed_samples():
                if sample["PROGRAM"] == FALCO_PROGRAM:
                    possible_anomaly = self.__handle_falco_entry(sample)
                    if possible_anomaly:
                        anomalies.append(possible_anomaly)
                elif sample["PROGRAM"] == SRPIO_PROGRAM:
                    # TODO process
                    pass
        except Exception:
            logger.exception(f"Error while retrieving anomalies!")
        return anomalies
