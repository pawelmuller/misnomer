from termcolor import colored


class MisnomerException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = colored(f"{' Encountered error ':=^80}\n{message}", "red")
        super(MisnomerException, self).__init__(self.message)


class MisnomerExecutiveNotFoundError(MisnomerException, FileNotFoundError):
    def __init__(self, path: str):
        self.message = f"File '{path}' with the executive could not be found."
        super(MisnomerExecutiveNotFoundError, self).__init__(self.message)


class MisnomerEncodingError(MisnomerException, ValueError):
    def __init__(self, *args, **kwargs):
        super(MisnomerEncodingError, self).__init__(args, kwargs)
