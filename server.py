from socket import *
import sys
import concurrent.futures

MESSAGE_LENGTH = 255


class Config:
    def __init__(self, port: int, max_threads: int) -> None:
        self.port = port
        self.max_threads = max_threads


class Error:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
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
    print("mam parametry: {}".format(str(args)))
    if len(args) < 3:
        return [
            None,
            Error(code=1, message="musis predat port a pocet vlaken jako parametry"),
        ]

    string_port = args[1]
    string_max_threads = args[2]
    if not string_port.isnumeric() or not string_max_threads.isnumeric():
        return [
            -1,
            Error(code=2, message="musis zadat port i vlakna nezaporny cely cislo"),
        ]

    port = int(string_port)
    max_threads = int(string_max_threads)
    print("zadany port: {}, pocet vclaken: {}".format(port, max_threads))

    return [Config(port=port, max_threads=max_threads), None]


def process_message(connection: socket):
    data = connection.recv(MESSAGE_LENGTH)
    if not data:
        connection.close()
        return 1

    print("received message: {}".format(data.decode()))
    reversed_message = data[::-1]  # decoding and reversing the message
    connection.send(reversed_message)
    connection.close()
    return 0


def run(config: Config):
    with socket(AF_INET, SOCK_STREAM) as s:
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(("127.0.0.1", config.port))
        s.listen(0)

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=config.max_threads
        ) as executor:
            while True:
                connection, address = s.accept()
                print("Received connection from " + str(address))
                connection.settimeout(60)
                executor.submit(process_message, connection)


port, error = parse_config(sys.argv)
if error:
    print(error.message)
    exit(error.code)

run(port)
