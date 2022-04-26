from io import TextIOWrapper

from utils.exceptions.exceptions import MisnomerExecutiveNotFoundError, MisnomerEncodingError
from utils.position import Position


class SourceReader:
    _END_OF_LINE = "\n"

    def __init__(self, source_path: str):
        self._source_path: str = source_path
        self._position = Position()
        self._source: TextIOWrapper
        self._code: str
        self._load_source()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._source.close()

    def _load_source(self):
        try:
            self._source = open(self._source_path, "r", encoding="utf-8")
            self._code = self._source.read()
        except FileNotFoundError as error:
            raise MisnomerExecutiveNotFoundError(self._source_path)
        except ValueError as error:
            raise MisnomerEncodingError(error)

    def get_next_character(self) -> str:
        character = self._code[self._position.character]
        if character == SourceReader._END_OF_LINE:
            self._position.line += 1
            self._position.column = 0
        else:
            self._position.column += 1

        self._position.character += 1
        return character

    def get_position(self):
        return self._position
