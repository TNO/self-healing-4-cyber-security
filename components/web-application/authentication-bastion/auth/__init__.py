# encoding: utf-8

import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

CONFIG_NAME_MAPPER = {
    "development": "auth.config.DevelopmentConfig",
    "production": "auth.config.ProductionConfig",
}


def create_app(flask_config_name=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application.
    """
    # This is a workaround for Alpine Linux (musl libc) quirk:
    # https://github.com/docker-library/python/issues/211
    import threading

    threading.stack_size(2 * 1024 * 1024)

    app = Flask(__name__, **kwargs)

    env_flask_config_name = os.getenv("FLASK_CONFIG")
    if not env_flask_config_name and flask_config_name is None:
        flask_config_name = "local"
    elif flask_config_name is None:
        flask_config_name = env_flask_config_name
    else:
        if env_flask_config_name:
            assert env_flask_config_name == flask_config_name, (
                'FLASK_CONFIG environment variable ("%s") and flask_config_name argument '
                '("%s") are both set and are not the same.'
                % (env_flask_config_name, flask_config_name)
            )

    try:
        name_from_mapper = CONFIG_NAME_MAPPER[flask_config_name]
        app.config.from_object(name_from_mapper)
    except ImportError:
        raise

    if app.config["REVERSE_PROXY_SETUP"]:
        app.wsgi_app = ProxyFix(app.wsgi_app)

    return app
