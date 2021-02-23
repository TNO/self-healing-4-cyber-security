import logging
from collections import defaultdict
from typing import List, Dict

from sh4cs_common.constants import get_epoch_time
from sh4cs_common.models import FailedLoginAttempt, FailedLoginAnomaly

logger = logging.getLogger(__name__)


class EventManager:
    def __init__(self, max_size=1000, minute_frequency_threshold=5):
        self._max_size = max_size
        self._minute_frequency_threshold = minute_frequency_threshold
        self._event_container: Dict[str, List[FailedLoginAttempt]] = defaultdict(list)

    def add_event(self, auth_model: FailedLoginAttempt):
        # Always add the latest event
        # TODO include the container id when creating the key to store attempts
        self._event_container[auth_model.get_username()].append(auth_model)

        # After adding event, make sure that we go back to max size
        # Start at the beginning and remove the earliest event
        if (
            self._max_size
            and len(self._event_container[auth_model.get_username()]) > self._max_size
        ):
            self._event_container[auth_model.get_username()].pop(0)

    @staticmethod
    def _count_events_in_window(
        sliding_window: List[FailedLoginAttempt], start_time: int, end_time: int
    ) -> int:
        return len(
            [
                event
                for event in sliding_window
                if start_time <= event.get_timestamp_epoch() <= end_time
            ]
        )

    def get_anomalies(self) -> List[FailedLoginAnomaly]:
        anomalies = []

        for username, failed_attempt_list in self._event_container.items():
            # We have not received enough events that could warrant an anomaly in the first place
            if len(failed_attempt_list) < self._minute_frequency_threshold:
                continue

            current_time = get_epoch_time()
            event_count_in_window = self._count_events_in_window(
                failed_attempt_list, start_time=current_time - 60, end_time=current_time
            )
            if event_count_in_window > self._minute_frequency_threshold:
                # Get one of the recorded attempts and grab the container id it came from
                # Since there must be events, we do not have to check size and just grab the latest
                # Grabbing the first could be a problem since we pop this position
                affected_container = failed_attempt_list[-1].get_affected_container()
                anomalies.append(
                    FailedLoginAnomaly(current_time, username, affected_container)
                )

        return anomalies
