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


class MisnomerParserNoIfStatementBlockException(MisnomerParserNoStatementBlockException):
    def __init__(self, position: Position):
        details = f"if statement"
        super(MisnomerParserNoIfStatementBlockException, self).__init__(details, position)


class MisnomerParserNoElseStatementBlockException(MisnomerParserNoStatementBlockException):
    def __init__(self, position: Position):
        details = f"else statement"
        super(MisnomerParserNoElseStatementBlockException, self).__init__(details, position)


class MisnomerParserNoWhileStatementBlockException(MisnomerParserNoStatementBlockException):
    def __init__(self, position: Position):
        details = f"while loop"
        super(MisnomerParserNoWhileStatementBlockException, self).__init__(details, position)


class MisnomerParserNoConditionException(MisnomerParserException):
    def __init__(self, details: str, position: Position):
        message = f"There is no condition for {details}."
        super(MisnomerParserNoConditionException, self).__init__(position, message, give_position=True)


class MisnomerParserNoIfConditionException(MisnomerParserNoConditionException):
    def __init__(self, position: Position):
        details = f"if statement"
        super(MisnomerParserNoIfConditionException, self).__init__(details, position)


class MisnomerParserNoWhileConditionException(MisnomerParserNoConditionException):
    def __init__(self, position: Position):
        details = f"while statement"
        super(MisnomerParserNoWhileConditionException, self).__init__(details, position)


class MisnomerParserNoInstructionsException(MisnomerParserException):
    def __init__(self, details: str, position: Position):
        message = f"There are no instructions for {details}."
        super(MisnomerParserNoInstructionsException, self).__init__(position, message, give_position=True)


class MisnomerParserNoIfInstructionsException(MisnomerParserNoConditionException):
    def __init__(self, position: Position):
        details = f"if statement"
        super(MisnomerParserNoIfInstructionsException, self).__init__(details, position)


class MisnomerParserNoWhileInstructionsException(MisnomerParserNoConditionException):
    def __init__(self, position: Position):
        details = f"while statement"
        super(MisnomerParserNoWhileInstructionsException, self).__init__(details, position)


class MisnomerParserNoExpressionException(MisnomerParserException):
    def __init__(self, current_token: TokenType, position: Position):
        message = f"There is no valid expression after {current_token}."
        super(MisnomerParserNoExpressionException, self).__init__(position, message, give_position=True)


class MisnomerParserNoSecondRelationalExpressionException(MisnomerParserException):
    def __init__(self, current_token: TokenType, position: Position):
        message = f"There is no second relational expression after {current_token}."
        super(MisnomerParserNoSecondRelationalExpressionException, self).__init__(position, message, give_position=True)


