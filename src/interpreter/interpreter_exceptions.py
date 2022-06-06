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
