import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

# From https://stackoverflow.com/questions/46457179/python3-cannot-import-name-cached-property

import logging.config
import os

from flask import Blueprint, redirect
from flask_cors import CORS
from backend.api.container import ns as bundle_namespace

from backend import create_app
from backend.api.restplus import api

log_config = {
    "version": 1,
    "disable_existing_loggers": "False",
    "formatters": {
        "defaultFormatter": {
            "format": "%(asctime)s.%(msecs)d %(filename)s: %(funcName)s: %(message)s",
            "datefmt": "%Y/%m/%d %H:%M:%S",
        }
    },
    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "defaultFormatter",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {"level": "DEBUG", "handlers": ["consoleHandler"], "propagate": False},
        "backend": {
            "level": "DEBUG",
            "handlers": ["consoleHandler"],
            "propagate": False,
        },
        "server": {
            "level": "DEBUG",
            "handlers": ["consoleHandler"],
            "propagate": False,
        },
        "__main__": {  # if __name__ == '__main__'
            "handlers": ["consoleHandler"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}

try:
    logging.config.dictConfig(log_config)
except Exception as e:
    raise RuntimeError("Failed to setup logging")

logger = logging.getLogger()


def initialize_api(flask_app):
    blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
    api.init_app(blueprint)

    api.add_namespace(bundle_namespace)
    flask_app.register_blueprint(blueprint)

    return flask_app


def main():
    environment = os.environ.get("SERVER_ENVIRONMENT")
    if not environment:
        environment = "development"
        os.environ["SERVER_ENVIRONMENT"] = environment

    app = create_app(environment)
    CORS(app)

    @app.route("/")
    def index():
        return redirect("api/v1/doc/")

    @app.context_processor
    def inject_dict_for_all_templates():
        # Use this function to make data available to all templates
        # https://stackoverflow.com/questions/31750655/pass-variables-to-all-jinja2-templates-with-flask
        return {}

    app = initialize_api(app)

    # This is the end point of the app, after this it will detach, place code before this
    app.run(
        host="0.0.0.0",
        debug=app.config["FLASK_DEBUG"],
        port=app.config["FLASK_PORT"],
    )


if __name__ == "__main__":
    main()
