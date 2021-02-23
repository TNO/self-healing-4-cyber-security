# pylint: disable=too-few-public-methods,invalid-name,missing-docstring
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(object):
    # Flask settings
    FLASK_DEBUG = True  # Do not use debug mode in production
    ENV = "development"

    # Flask-Restplus settings
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    ERROR_404_HELP = False

    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    REVERSE_PROXY_SETUP = os.getenv("EXAMPLE_API_REVERSE_PROXY_SETUP", False)

    STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")

    SWAGGER_UI_JSONEDITOR = True
    SWAGGER_UI_OAUTH_CLIENT_ID = "documentation"
    SWAGGER_UI_OAUTH_REALM = "SH4CS docker proxy documentation"
    SWAGGER_UI_OAUTH_APP_NAME = "SH4CS docker proxy documentation"
    SECRET_KEY = "secret!"
    FLASK_PORT = 5000


class ProductionConfig(BaseConfig):
    FLASK_DEBUG = False
    ENV = "production"


class DevelopmentConfig(BaseConfig):
    ASYNC_MODE = None
    FLASK_DEBUG = True
