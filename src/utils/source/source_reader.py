from io import TextIOWrapper

from utils.exceptions.exceptions import ExecutiveNotFoundError


class SourceReader:
    class Position:
        def __init__(self, line=0, column=0):
            self.line = line
            self.column = column

    def __init__(self, source_path: str):
        self._source_path: str = source_path
        self._position = SourceReader.Position()
        self._source: TextIOWrapper
        self._load_source()

    def _load_source(self):
        try:
            with open(self._source_path, "r") as file:
                self._source = file
        except FileNotFoundError as error:
            raise ExecutiveNotFoundError(error)

    def get_next_character(self) -> str:
        bytes_to_read = 1
        character = self._source.read(bytes_to_read)
        if character == "\n":
            self._position.line += 1
            self._position.char = 0
        else:
            self._position.char += 1
        return character
