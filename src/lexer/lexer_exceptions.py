from utils.exceptions import MisnomerException
from utils.position import Position


class MisnomerLexerException(MisnomerException):
    def __init__(self, position: Position, message: str = "", give_position=True):
        if give_position:
            message = f"Exception during scanning at: {position}.\n{message}"
        else:
            message = f"Exception during scanning.\n{message}"
        super(MisnomerLexerException, self).__init__(message)


class MisnomerLexerUnterminatedStringException(MisnomerLexerException):
    def __init__(self, position: Position, message: str = ""):
        message = "The string seems to be terminated incorrectly."
        super(MisnomerLexerUnterminatedStringException, self).__init__(position, message, give_position=False)


class MisnomerLexerStringBuildExceededLengthException(MisnomerLexerException):
    def __init__(self, position: Position, max_length: int, message: str = ""):
        message = f"The string exceeded the maximum length limit ({max_length})."
        super(MisnomerLexerStringBuildExceededLengthException, self).__init__(position, message, give_position=False)


class MisnomerLexerNumericBuildException(MisnomerLexerException):
    def __init__(self, position: Position, message: str = ""):
        message = f"Failed to build a number: {message}"
        super(MisnomerLexerNumericBuildException, self).__init__(position, message)
