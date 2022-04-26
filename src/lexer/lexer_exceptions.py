from utils.exceptions import MisnomerException
from utils.position import Position


class MisnomerLexerException(MisnomerException):
    def __init__(self, position: Position, message: str = ""):
        message = f"Exception during scanning at: {position}.\n{message}"
        super(MisnomerLexerException, self).__init__(message)


class MisnomerLexerUnterminatedStringException(MisnomerLexerException):
    def __init__(self, position: Position, message: str = ""):
        message = "The string seems not to be terminated correctly."
        super(MisnomerLexerUnterminatedStringException, self).__init__(position, message)
