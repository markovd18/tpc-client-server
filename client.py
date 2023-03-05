import sys
from socket import *

from shared import MAX_DATA_LENGTH, MAX_MESSAGE_LENGTH, Error, parse_unsigned_int


class Config:
    def __init__(self, port: int, message: str) -> None:
        self.port = port
        self.message = message


def parse_config(args: list[str]) -> tuple[Config | None, Error | None]:
    """Parses server configuration from list of arguments.

    Args:
        args (list[str]): list of arguments as strings, intended to be passed from CLI

    Returns:
        tuple[Config | None, Error | None]: A tuple of possible server configuration and error. An ``Error`` object
        is returned when there is an error while parsing the arguments or they are of invalid value. If parsing succeeded,
        error is ``None`` and ``Config`` object is present.
    """
    print("Parsing parameters: {}".format(str(args)))
    args_len = len(args)
    if args_len < 3:
        return (
            None,
            Error(
                code=2,
                message="Server port and message to send need to be passed as arguments.",
            ),
        )

    port, port_success = parse_unsigned_int(args[1])
    if not port_success:
        return (
            None,
            Error(code=1, message="Server port has to be an unsigned integer."),
        )

    message = args[2]
    if len(message) > MAX_MESSAGE_LENGTH:
        print(
            "WARNING: Maximum message length is {}. Trimming...".format(
                str(MAX_MESSAGE_LENGTH)
            )
        )
        message = message[:MAX_MESSAGE_LENGTH]

    return (Config(port=port, message=message), None)


def run(config: Config):
    s = socket(AF_INET, SOCK_STREAM)  # IPv4, TCP
    s.connect(("127.0.0.1", config.port))  # Connect (host, port)

    data = len(config.message).to_bytes(1, sys.byteorder) + bytes(
        config.message, encoding="utf8"
    )
    print("sending message: {}".format(data))
    s.send(data)  # Send request

    data = s.recv(MAX_DATA_LENGTH)  # Get response
    print("Response: " + str(data))

    s.close()


config, error = parse_config(sys.argv)
if error:
    print(error.message)
    exit(error.code)

run(config)
