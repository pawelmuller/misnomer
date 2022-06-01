from lexer.token.token_type import TokenType
from utils.exceptions import MisnomerException
from utils.position import Position


class MisnomerTokenException(MisnomerException):
    def __init__(self, position: Position, message: str = "", give_position=True):
        if give_position:
            message = f"Exception during creating token at: {position}.\n{message}"
        else:
            message = f"Exception during creating token.\n{message}"
        super(MisnomerTokenException, self).__init__(message)


class MisnomerTokenInappropriateTypeException(MisnomerTokenException):
    def __init__(self, value_type: type, token_type: TokenType, position: Position):
        message = f"The given value type ({value_type}) does not match given token type ({token_type})."
        super(MisnomerTokenInappropriateTypeException, self).__init__(position, message, give_position=False)
