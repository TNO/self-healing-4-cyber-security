import logging
import sys

from flask_restx import Api

logger = logging.getLogger(__name__)

api = Api(
    version="1.0",
    title="SH4CS Docker Proxy API",
    description="SH4CS Docker Proxy API",
    doc="/doc/",
)


@api.errorhandler
def default_error_handler(e: Exception):
    message = "An unhandled exception occurred"
    exc_info = sys.exc_info()

    logger.error(f"{message}:{str(e)}", exc_info=exc_info)

    return {"message": message}, 500
