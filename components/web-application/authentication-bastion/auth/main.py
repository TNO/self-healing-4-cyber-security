import logging
import time

from flask import Blueprint
from flask import request
from flask_cors import CORS
from sh4cs_common.constants import get_lymphocite_registration_channel
from sh4cs_common.utils import setup_logging, get_container_name

from auth import create_app
from auth.api.v1 import api as api_v1
from auth.api.v1.redis_instance import redis_instance

logger = setup_logging(package_name="auth", level=logging.getLevelName(logging.DEBUG))


def register_myself_in_redis_for_lymphocite():
    container_name = get_container_name()
    logger.info(f"Registering container with name: '{container_name}'")
    label = "auth_bastion"

    redis_instance.get_redis().sadd(get_lymphocite_registration_channel(), label)
    redis_instance.get_redis().set(label, container_name)


def initialize_api_v1(flask_app):
    blueprint = Blueprint("api_v1", __name__, url_prefix="/api/v1")
    api_v1.init_app(blueprint)
    flask_app.register_blueprint(blueprint)


def main():
    app = create_app("production")
    CORS(app)

    @app.before_request
    def log_path():
        logger.debug(
            ">>> {0} - {1} {2}".format(
                request.remote_addr, request.method, request.path
            )
        )

    initialize_api_v1(app)
    while not redis_instance.wait_for_redis():
        time.sleep(1)
    register_myself_in_redis_for_lymphocite()

    host = "0.0.0.0"

    logger.info(">>>>> Starting server at http://{0}:5000/api/ <<<<<".format(host))

    app.run(host=host, debug=app.config["FLASK_DEBUG"])


if __name__ == "__main__":
    main()
