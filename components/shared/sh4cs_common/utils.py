import functools
import logging
import logging.config
import os


@functools.lru_cache(maxsize=1)
def get_container_name() -> str:
    return os.environ.get("HOSTNAME")


def setup_logging(package_name: str, level: str) -> logging.Logger:
    log_config = {
        "version": 1,
        "disable_existing_loggers": "True",
        "formatters": {
            "defaultFormatter": {
                "format": "%(asctime)s.%(msecs)d %(filename)s: %(funcName)s: %(message)s",
                "datefmt": "%Y/%m/%d %H:%M:%S",
            },
        },
        "handlers": {
            "consoleHandler": {
                "class": "logging.StreamHandler",
                "level": f"{level}",
                "formatter": "defaultFormatter",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "loggers": {
            "": {
                "level": f"{level}",
                "handlers": ["consoleHandler"],
                "propagate": False,
            },
            f"{package_name}": {
                "level": f"{level}",
                "handlers": ["consoleHandler"],
                "propagate": False,
            },
            "__main__": {  # if __name__ == '__main__'
                "handlers": ["consoleHandler"],
                "level": f"{level}",
                "propagate": False,
            },
        },
    }

    try:
        logging.config.dictConfig(log_config)
    except Exception:
        raise RuntimeError("Failed to setup logging")

    return logging.getLogger()
