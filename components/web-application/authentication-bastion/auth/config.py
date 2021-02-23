# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(object):
    # Flask settings    # Checking if that works for development.
    FLASK_DEBUG = False  # Do not use debug mode in production
    ENV = "production"

    REVERSE_PROXY_SETUP = os.getenv("REVERSE_PROXY_SETUP", False)

    # Flask-Restplus settings
    SWAGGER_UI_DOC_EXPANSION = "list"
    SWAGGER_UI_JSONEDITOR = True

    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    ERROR_404_HELP = False

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

    # Authentication setting
    API_TOKEN = "LETS_KEEP_THIS_SECRET"
    MANAGEMENT_API_TOKEN = "LETS_KEEP_THIS_SECRET"

    # Master secret
    SERVER_SECRET = "LETS_KEEP_THIS_SECRET"


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    FLASK_DEBUG = True
    ENV = "development"
