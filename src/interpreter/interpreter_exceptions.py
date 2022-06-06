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
