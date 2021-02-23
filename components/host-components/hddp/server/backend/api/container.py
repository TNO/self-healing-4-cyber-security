import datetime
import http
import logging

import pytz
from docker.errors import APIError, NotFound
from docker.models.containers import Container
from flask import request
from flask_restx import Resource, Namespace, reqparse

from backend.api.business.container import (
    docker_connection_proxy,
    parse_docker_started_at_time,
    is_container_running,
    container_status,
)

CONTAINER_IDENTIFIER = "container_identifier"

logger = logging.getLogger(__name__)

ns = Namespace("docker", description="Operations related to Docker")

container_name_args = reqparse.RequestParser()
container_name_args.add_argument(CONTAINER_IDENTIFIER, required=True)


def error_400_no_container_id():
    return (
        "No container identifier passed!",
        http.HTTPStatus.BAD_REQUEST.real,
    )


def error_404_non_existent_container_id(container_identifier: str):
    return (
        f"Could not find container with identifier='{container_identifier}'",
        http.HTTPStatus.NOT_FOUND.real,
    )


def error_500_internal_server_error():
    return (
        "Error occurred while interacting with the docker API",
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
    )


def error_409_container_non_running_state(container_identifier: str):
    return (
        f"Container with identifier='{container_identifier}' was not in right state",
        http.HTTPStatus.CONFLICT.real,
    )


@ns.route("/remove")
class RemoveDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            container: Container = docker_connection_proxy.find_container(
                container_identifier
            )
            logger.debug(
                f"Found container with name='{container.name}' using input container identifier='{container_identifier}'"
            )
            if is_container_running(container):
                logger.warning(
                    f"Container with name='{container.name}' was running when trying to delete, executing stop"
                )
                container.stop()

            container.remove(force=True)
            return {}, http.HTTPStatus.OK.real
        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


@ns.route("/exists")
class RemoveDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            docker_connection_proxy.find_container(container_identifier)
            return {}, http.HTTPStatus.OK.real
        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


@ns.route("/status")
class StatusDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            container: Container = docker_connection_proxy.find_container(
                container_identifier
            )
            logger.debug(
                f"Found container with name='{container.name}' using input container identifier='{container_identifier}'"
            )
            return {"status": container_status(container)}, http.HTTPStatus.OK.real
        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


@ns.route("/kill")
class KillDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.CONFLICT.real,
        "Container was not in right state when wanting to execute command",
    )  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            container: Container = docker_connection_proxy.find_container(
                container_identifier
            )
            logger.debug(
                f"Found container with name='{container.name}' using input container identifier='{container_identifier}'"
            )
            if not is_container_running(container):
                logger.warning(
                    f"Container with name='{container.name}' was not in running state, can not execute kill"
                )
                return error_409_container_non_running_state(container_identifier)

            container.kill()
            return {}, http.HTTPStatus.OK.real

        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


@ns.route("/stop")
class StopDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.CONFLICT.real,
        "Container was not in right state when wanting to execute command",
    )  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            container: Container = docker_connection_proxy.find_container(
                container_identifier
            )
            logger.debug(
                f"Found container with name='{container.name}' using input container identifier='{container_identifier}'"
            )
            if not is_container_running(container):
                logger.warning(
                    f"Container with name='{container.name}' was not in running state, can not execute stop"
                )
                return error_409_container_non_running_state(container_identifier)

            container.stop()
            return {}, http.HTTPStatus.OK.real

        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


@ns.route("/pause")
class PauseDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.CONFLICT.real,
        "Container was not in right state when wanting to execute command",
    )  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            container: Container = docker_connection_proxy.find_container(
                container_identifier
            )
            logger.debug(
                f"Found container with name='{container.name}' using input container identifier='{container_identifier}'"
            )
            if not is_container_running(container):
                logger.warning(
                    f"Container with name='{container.name}' was not in running state, can not execute pause"
                )
                return error_409_container_non_running_state(container_identifier)

            container.pause()
            return {}, http.HTTPStatus.OK.real

        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


@ns.route("/uptime")
class UptimeDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.CONFLICT.real,
        "Container was not in right state when wanting to execute command",
    )  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            # a_container.attrs['State']['StartedAt']
            # >>> abc
            # '2020-10-28T14:32:23.518166769Z'

            container: Container = docker_connection_proxy.find_container(
                container_identifier
            )
            logger.debug(
                f"Found container with name='{container.name}' using input container identifier='{container_identifier}'"
            )
            started_at_datetime = parse_docker_started_at_time(
                container.attrs["State"]["StartedAt"]
            )

            current_time = get_utc_now()
            uptime_in_seconds = (current_time - started_at_datetime).total_seconds()

            return {"uptime": int(uptime_in_seconds)}, http.HTTPStatus.OK.real
        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


@ns.route("/name")
class NameDockerItem(Resource):
    @ns.expect(container_name_args)
    @ns.response(http.HTTPStatus.OK.real, "Success")  # Possible error codes
    @ns.response(
        http.HTTPStatus.INTERNAL_SERVER_ERROR.real, "Failure while processing request"
    )  # Possible error codes
    def post(self):
        args = container_name_args.parse_args(request)
        container_identifier = args.get(CONTAINER_IDENTIFIER)
        if not container_identifier:
            return error_400_no_container_id()

        try:
            container: Container = docker_connection_proxy.find_container(
                container_identifier
            )
            logger.debug(
                f"Found container with name='{container.name}' using input container identifier='{container_identifier}'"
            )

            return {"name": container.name}, http.HTTPStatus.OK.real
        except NotFound:
            return error_404_non_existent_container_id(container_identifier)
        except APIError:
            logger.exception(f"Could not finish processing request")
            return error_500_internal_server_error()


def get_utc_now() -> datetime.date:
    current_time = datetime.datetime.utcnow()
    return current_time.replace(tzinfo=pytz.utc)
