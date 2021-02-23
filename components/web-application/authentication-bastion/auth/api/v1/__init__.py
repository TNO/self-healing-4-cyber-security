import logging

from flask import url_for, jsonify
from flask_restplus import Api

from auth.api.v1.user import api as api_user

logger = logging.getLogger(__name__)


class CustomAPI(Api):
    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`) :rtype: str
        """
        return url_for(self.endpoint("specs"), _external=False)


api = CustomAPI(version="1.0", title="Authentication Service API", description="")

api.add_namespace(api_user)


@api.errorhandler
def default_error_handler(ex):
    logger.exception(ex)
    return jsonify({"message": "An unhandled exception occurred"})
