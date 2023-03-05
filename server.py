from socket import *
import sys
import concurrent.futures
from shared import Error, parse_unsigned_int, MAX_DATA_LENGTH

MAX_THREAD_COUNT = 6


class Config:
    def __init__(self, port: int = 8080, max_threads: int = 3) -> None:
        self.port = port
        self.max_threads = max_threads


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
    if args_len < 2:
        print("Initiating with default configuration...")
        return (Config(), None)

    port, port_success = parse_unsigned_int(args[1])
    if args_len < 3:
        return (
            (Config(port=port), None)
            if port_success
            else (None, Error(code=1, message="Port has to be an unsigned integer."))
        )

    max_threads, max_threads_success = parse_unsigned_int(args[2])
    if not max_threads_success:
        return (
            None,
            Error(code=1, message="Thread count has to be an unsigned integer."),
        )

    if max_threads > MAX_THREAD_COUNT:
        print(
            "WARNING: Maximum number of allowed threads is {}, falling back this value.".format(
                MAX_THREAD_COUNT
            )
        )
        max_threads = MAX_THREAD_COUNT

    return (
        (Config(port=port, max_threads=max_threads), None)
        if max_threads_success
        else (
            None,
            Error(code=1, message="Thread count has to be an unsigned integer."),
        )
    )


def process_message(connection: socket):
    with connection:
        data = connection.recv(MAX_DATA_LENGTH)
        if not data:
            return 1

        message_length = data[0:1]  # slice of single byte - message length
        message = data[1:]  # first byte is message length which
        print("received message: {}".format(message))
        reversed_message = message[::-1]  # reversing the message
        print("sending back message: {}".format(reversed_message))
        connection.send(message_length + reversed_message)
        return 0


def run(config: Config):
    with socket(AF_INET, SOCK_STREAM) as s:
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(("127.0.0.1", config.port))
        s.listen(0)
        print(
            "Listening on port '{}'.\nMaximum number of threads is set to {}.".format(
                config.port, config.max_threads
            )
        )
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=config.max_threads
        ) as executor:
            while True:
                connection, address = s.accept()
                print("Received connection from " + str(address))
                connection.settimeout(60)
                executor.submit(process_message, connection)


config, error = parse_config(sys.argv)
if error:
    print(error.message)
    exit(error.code)

run(config)
