import time
import os

__REDIS_CHANNEL_FAILED_LOGIN = "auth_logs"
__REDIS_CHANNEL_OUTPUT_ANOMALIES = "auth_anomalies"
__REDIS_CHANNEL_LYMPHOCITE_REGISTRATION = "lymphocite_registration"


def get_auth_failed_attempts_channel() -> str:
    """
    Reads REDIS_OUTPUT_CHANNEL from local environment, if not set returns auth_logs
    """
    return os.environ.get("REDIS_OUTPUT_CHANNEL", __REDIS_CHANNEL_FAILED_LOGIN)


def get_auth_anomalies_channel() -> str:
    """
    Reads REDIS_MONITOR_CHANNEL from local environment, if not set returns auth_anomalies
    """
    return os.environ.get("REDIS_MONITOR_CHANNEL", __REDIS_CHANNEL_OUTPUT_ANOMALIES)


def get_lymphocite_registration_channel() -> str:
    """
    Reads REDIS_REGISTRATION_CHANNEL from local environment, if not set returns lymphocite_registration
    """
    return os.environ.get(
        "REDIS_REGISTRATION_CHANNEL", __REDIS_CHANNEL_LYMPHOCITE_REGISTRATION
    )


def get_epoch_time() -> int:
    return int(time.time())


# REDIS_HOST=test-redis
# REDIS_MONITOR_CHANNEL=auth_logs
# REDIS_OUTPUT_CHANNEL="anomalies"
# MINUTE_FREQUENCY_THRESHOLD=5
# ALERT_MESSAGE=brute_force_detected
