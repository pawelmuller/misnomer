from utils.exceptions import MisnomerException
from utils.position import Position


class MisnomerInterpreterException(MisnomerException):
    def __init__(self, position: Position, message: str = "", give_position=True):
        if give_position:
            message = f"Exception during interpreting at: {position}.\n{message}"
        else:
            message = f"Exception during interpreting.\n{message}"
        super(MisnomerInterpreterException, self).__init__(message)


class MisnomerInterpreterNoMainFunctionException(MisnomerInterpreterException):
    def __init__(self, position: Position):
        message = f"Main function has not been found."
        super(MisnomerInterpreterNoMainFunctionException, self).__init__(position, message, give_position=False)


class MisnomerInterpreterDeclarationException(MisnomerInterpreterException):
    def __init__(self, name: str, position: Position):
        message = f"Declaration error with {name}."
        super(MisnomerInterpreterDeclarationException, self).__init__(position, message, give_position=False)


class MisnomerInterpreterArgumentsNumberDoesNotMatchException(MisnomerInterpreterException):
    def __init__(self, expected_arguments_number: int, got_arguments_number: int, name: str, position: Position):
        message = f"Number of arguments for function {name} does not match.\n"
        message += f"Expected: {expected_arguments_number}, got: {got_arguments_number}."
        super(MisnomerInterpreterArgumentsNumberDoesNotMatchException, self).__init__(position, message,
                                                                                      give_position=False)


class MisnomerInterpreterIdentifierDoesNotExistException(MisnomerInterpreterException):
    def __init__(self, identifier_type: str, name: str, position: Position):
        message = f"{identifier_type} {name} does not exist.\n"
        super(MisnomerInterpreterIdentifierDoesNotExistException, self).__init__(position, message, give_position=True)


class MisnomerInterpreterFunctionDoesNotExistException(MisnomerInterpreterIdentifierDoesNotExistException):
    def __init__(self, name: str, position: Position):
        identifier_type = "Function"
        super(MisnomerInterpreterFunctionDoesNotExistException, self).__init__(identifier_type, name, position)


class MisnomerInterpreterVariableDoesNotExistException(MisnomerInterpreterIdentifierDoesNotExistException):
    def __init__(self, name: str, position: Position):
        identifier_type = "Variable"
        super(MisnomerInterpreterVariableDoesNotExistException, self).__init__(identifier_type, name, position)


class MisnomerInterpreterCouldNotNegateExpressionException(MisnomerInterpreterException):
    def __init__(self, expression, position: Position):
        message = f"Could not negate {expression.__class__.__name__} expression.\n"
        super(MisnomerInterpreterCouldNotNegateExpressionException, self).__init__(position, message,
                                                                                   give_position=True)


class MisnomerInterpreterBadOperandTypeException(MisnomerInterpreterException):
    def __init__(self, operand: str, expression, position: Position):
        message = f"Bad operand '{operand}' for {expression.__class__.__name__} expression.\n"
        super(MisnomerInterpreterBadOperandTypeException, self).__init__(position, message, give_position=True)


class MisnomerInterpreterCastingException(MisnomerInterpreterException):
    def __init__(self, cast_type: str, expression, position: Position):
        message = f"Cannot cast '{expression.__class__.__name__}' to {cast_type}.\n"
        super(MisnomerInterpreterCastingException, self).__init__(position, message, give_position=True)


class MisnomerInterpreterCastingBuiltinException(MisnomerInterpreterCastingException):
    def __init__(self, cast_type: str, expression):
        self.cast_type = cast_type
        self.expression = expression


class MisnomerInterpreterVariableAssignmentException(MisnomerInterpreterException):
    def __init__(self, value_type: type, variable_type: type, variable_name: str, position: Position):
        message = f"Cannot assign value of type {value_type} to variable '{variable_name}' of type {variable_type}.\n"
        super(MisnomerInterpreterVariableAssignmentException, self).__init__(position, message, give_position=True)
