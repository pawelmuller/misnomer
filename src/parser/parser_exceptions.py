from lexer.token.token_type import TokenType
from utils.exceptions import MisnomerException
from utils.position import Position


class MisnomerParserException(MisnomerException):
    def __init__(self, position: Position, message: str = "", give_position=True):
        if give_position:
            message = f"Exception during parsing at: {position}.\n{message}"
        else:
            message = f"Exception during parsing.\n{message}"
        super(MisnomerParserException, self).__init__(message)


class MisnomerParserUnexpectedTokenException(MisnomerParserException):
    def __init__(self, expected_token: TokenType, actual_token: TokenType, position: Position):
        message = f"Expected token {expected_token}, but got {actual_token} instead."
        super(MisnomerParserUnexpectedTokenException, self).__init__(position, message, give_position=True)


class MisnomerParserNoStatementBlockException(MisnomerParserException):
    def __init__(self, details: str, position: Position):
        message = f"There is no statement block for {details}."
        super(MisnomerParserNoStatementBlockException, self).__init__(position, message, give_position=True)


class MisnomerParserNoFunctionStatementBlockException(MisnomerParserNoStatementBlockException):
    def __init__(self, function_name: str, position: Position):
        details = f"{function_name} function"
        super(MisnomerParserNoFunctionStatementBlockException, self).__init__(details, position)
