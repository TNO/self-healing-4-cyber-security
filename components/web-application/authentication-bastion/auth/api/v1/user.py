import logging
import time
from typing import Set

from flask import request
from flask_restplus import Namespace, Resource
from flask_restplus import reqparse
from itsdangerous import URLSafeSerializer
from sh4cs_common.constants import (
    get_epoch_time,
    get_auth_failed_attempts_channel,
)
from sh4cs_common.models import FailedLoginAttempt
from sh4cs_common.utils import get_container_name

from auth.api.v1.redis_instance import redis_instance
from auth.api.v1.token import TokenManager

POLICY_RESPONSE_PAYLOAD_TOKENS = "tokens"

logger = logging.getLogger(__name__)

USER_ID_KEY = "uuid"
USER_TOKEN_KEY = "token"
USER_PASSWORD_KEY = "password"

SAMPLE_USER_UUID = "82eab5f2-d574-11e9-bb65-2a2ae2dbcce4"
SAMPLE_SERVER_UUID = "901520d2-d574-11e9-bb65-2a2ae2dbcce4"
SUCCESS = "[Success]"
FAILED = "[Failed]"

api = Namespace(
    "user", description="Operations related to user and service authentication"
)

# users = { user@username: {user@password: x, user@uuid:y, user@token:z}}
users = {
    "sample_username": {
        USER_PASSWORD_KEY: "abc",
        USER_ID_KEY: SAMPLE_USER_UUID,
    }
}
# services = { service@uuid: [user@uuid]}
services = {SAMPLE_SERVER_UUID: [SAMPLE_USER_UUID]}

blocklist = set()

authorize_request = reqparse.RequestParser()
authorize_request.add_argument(
    "user_id", required=True, help="User ID matching the token"
)
authorize_request.add_argument(
    "server_id", required=True, help="Server ID to check against"
)
authorize_request.add_argument(
    "user_token", required=True, help="Token obtained with user matching User ID"
)

authentication_request = reqparse.RequestParser()
authentication_request.add_argument(
    "username", required=True, help="Username of an user"
)
authentication_request.add_argument(
    "password", required=True, help="Password corresponding to the username passed"
)

block_request = reqparse.RequestParser()
block_request.add_argument("username", required=True, help="Username of an user")

token_manager = TokenManager()


@api.route("/authorize")
class Authorize(Resource):
    @api.expect(authorize_request)
    def post(self):
        """
        Authenticate an user for a given service.
        """
        request_args = authorize_request.parse_args()

        # Verify user token
        user_token = get_token_from_request(request_args)
        if not user_token:
            logger.warning("Failed authorization attempt due to lack of token")
            return {"message": "Unauthorized"}, 401

        user_uuid = get_user_uuid_from_request(request_args)
        service_id = get_server_uuid_from_request(request_args)
        if not verify_user_is_authenticated(user_token, user_uuid):
            logger.warning(
                f"User {user_uuid} was not authorized to be using token {user_token}"
            )
            return {"message": "Unauthorized"}, 401

        if not is_user_authorized_for_service(user_token, user_uuid, service_id):
            logger.warning(
                f"User {user_uuid} was not authorized for {service_id} using token {user_token} "
            )
            return {"message": "Unauthorized"}, 401

        logger.debug(f"Authenticated {user_uuid} user for service {service_id}")
        return {"message": "Success"}, 200


@api.route("/login")
class Login(Resource):
    @api.expect(authentication_request)
    def post(self):
        """
        Authenticate an existing user
        """
        request_args = authentication_request.parse_args()
        username = get_username_from_request(request_args)
        password = get_password_from_request(request_args)

        if is_blocked(username):
            logger.debug(
                f"{FAILED} login attempt USERNAME={username} on blocked user, from IP={get_ip_for_request(request)}"
            )
            publish_failed_attempt_for_user(username)
            return {"message": "Unauthorized"}, 401

        if not verify_credentials(username, password):
            logger.warning(
                f"{FAILED} login attempt USERNAME={username} from IP={get_ip_for_request(request)}"
            )
            publish_failed_attempt_for_user(username)
            return {"message": "Unauthorized"}, 401

        logger.debug(f"Logging in {username}")

        token = generate_user_token(username)
        if set_token_for_user(username, token):
            logger.info(
                f"{SUCCESS} login attempt USERNAME={username} from IP={get_ip_for_request(request)}"
            )
            return {"message": "Success", USER_TOKEN_KEY: token}, 200

        return {"message": f"Was not able to store token for user {username}"}, 500


@api.route("/block")
class Block(Resource):
    @api.expect(block_request)
    def post(self):
        """
        Block an existing user
        """
        request_args = block_request.parse_args()
        username = get_username_from_request(request_args)
        if username not in users:
            logger.debug(
                f"USERNAME={username} does not exist from IP={get_ip_for_request(request)}"
            )
            return {"message": "Username does not exist"}, 400

        self.add_to_block_list(username)

        return {"message": f"Blocked {username}"}, 200

    @staticmethod
    def add_to_block_list(username):
        logger.debug(f"Blocking {username}")
        blocklist.add(username)


@api.route("/unblock")
class Unblock(Resource):
    @api.expect(block_request)
    def post(self):
        """
        Unblock an existing user
        """
        request_args = block_request.parse_args()
        username = get_username_from_request(request_args)
        if username not in users:
            logger.debug(
                f"USERNAME={username} does not exist from IP={get_ip_for_request(request)}"
            )
            return {"message": "Username does not exist"}, 400

        self.remove_from_block_list(username)

        return {"message": f"Unblocked {username}"}, 200

    @staticmethod
    def remove_from_block_list(username):
        logger.debug(f"Unblocking {username}")
        blocklist.remove(username)


def get_ip_for_request(current_request):
    if current_request.environ.get("X-Real-IP") is not None:
        return current_request.environ["X-Real-IP"]
    elif current_request.environ.get("HTTP_X_FORWARDED_FOR") is None:
        return current_request.environ["REMOTE_ADDR"]
    else:
        return current_request.environ["HTTP_X_FORWARDED_FOR"]


def verify_credentials(username: str, password: str) -> bool:
    for stored_username, values in users.items():
        if stored_username == username:
            return password == values[USER_PASSWORD_KEY]
    return False


def is_blocked(username: str) -> bool:
    return username in blocklist


def verify_user_is_authenticated(user_token: str, user_uuid: str) -> bool:
    for username, values in users.items():
        if values[USER_ID_KEY] == user_uuid:
            user_tokens = get_tokens_for_user(username)
            return user_token in user_tokens
    return False


def is_user_authorized_for_service(
    user_token: str, user_uuid: str, service_id: str
) -> bool:
    return _is_allowed_to_use_service(
        user_uuid, service_id
    ) and _is_token_valid_for_user(user_uuid, user_token)


def _is_allowed_to_use_service(user_uuid: str, service_id: str) -> bool:
    for service, authorized_user_ids in services.items():
        if service == service_id:
            return user_uuid in authorized_user_ids
    return False


def _is_token_valid_for_user(user_uuid: str, user_token: str) -> bool:
    for username, values in users.items():
        if values[USER_ID_KEY] == user_uuid:
            user_tokens = get_tokens_for_user(username)
            return user_token in user_tokens
    return False


def generate_user_token(username) -> str:
    """
    Generate a user token based on the user identifier.
    """
    serializer = URLSafeSerializer("SERVER-SECRET-IS-VERY-SECURE")
    token = serializer.dumps(
        {"id": username, "time": str(round(time.monotonic() * 1000))}
    )

    return token


def set_token_for_user(username: str, token: str) -> bool:
    for stored_username, values in users.items():
        if username == stored_username:
            return add_token_to_policy(username, token)
    return False


def publish_failed_attempt_for_user(username: str) -> bool:
    redis_instance.get_redis().publish(
        get_auth_failed_attempts_channel(),
        FailedLoginAttempt(get_epoch_time(), username, get_container_name()).to_redis(),
    )
    return True


def get_tokens_for_user(username: str) -> Set[str]:
    return token_manager.tokens_for_user(username)


def add_token_to_policy(username: str, token: str) -> bool:
    token_manager.add_token_for_user(username, token)
    return True


def get_token_from_request(request_args) -> str:
    return request_args.user_token


def get_user_uuid_from_request(request_args) -> str:
    return request_args.user_id


def get_username_from_request(request_args) -> str:
    return request_args.username


def get_password_from_request(request_args) -> str:
    return request_args.password


def get_server_uuid_from_request(request_args) -> str:
    return request_args.server_id
