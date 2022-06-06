from termcolor import colored


class MisnomerException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = colored(f"\n{' Encountered error ':=^80}\n{message}", "red")
        super(MisnomerException, self).__init__(self.message)


class MisnomerExecutiveNotFoundError(MisnomerException, FileNotFoundError):
    def __init__(self, path: str):
        self.message = f"File '{path}' with the executive could not be found."
        super(MisnomerExecutiveNotFoundError, self).__init__(self.message)


class MisnomerEncodingError(MisnomerException, ValueError):
    def __init__(self, message):
        self.message = f"You should use UTF-8 encoded text file as a source od the code.\nDetails: {message}"
        super(MisnomerEncodingError, self).__init__(self.message)
