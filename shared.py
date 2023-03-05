MAX_MESSAGE_LENGTH = 255
MAX_DATA_LENGTH = MAX_MESSAGE_LENGTH + 1
"""There is a message length information stored in the first byte of the data.
"""


class Error:
    def __init__(self, code: int, message: str) -> None:
        self.code = code
        self.message = message


def parse_unsigned_int(string: str) -> tuple[int | None, bool]:
    """Parses an unsigned integer value from string. Returns value and success flag.

    Args:
        string (str): string to parse

    Returns:
        tuple[int | None, bool]: possible unsigned int value and success flag - ``true`` if successfuly parsed, otherwise ``false``
    """
    return (int(string), True) if string.isnumeric() else (None, False)
