class MisnomerException(Exception):
    pass


class ExecutiveNotFoundError(FileNotFoundError, MisnomerException):
    pass
