from copy import copy
from io import TextIOWrapper

from lexer.dictionaries import EOF
from utils.exceptions.exceptions import MisnomerExecutiveNotFoundError, MisnomerEncodingError
from utils.position import Position


class SourceReader:
    _END_OF_LINE = "\n"

    def __init__(self):
        self._position = Position()

    def update_position(self, character: str):
        if character == SourceReader._END_OF_LINE:
            self._position.line += 1
            self._position.column = 0
        else:
            self._position.column += 1

        self._position.character += 1

    def get_position(self):
        return copy(self._position)


class FileSourceReader(SourceReader):
    def __init__(self, source_path: str):
        super().__init__()
        self._source_path: str = source_path
        self._source: TextIOWrapper
        self._load_source()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._source.close()

    def _load_source(self):
        try:
            self._source = open(self._source_path, "r", encoding="utf-8")
        except FileNotFoundError:
            raise MisnomerExecutiveNotFoundError(self._source_path)
        except ValueError or UnicodeDecodeError as error:
            raise MisnomerEncodingError(error)

    def get_next_character(self) -> str:
        if character := self._source.read(1):
            self.update_position(character)
            return character
        return EOF


class StringSourceReader(SourceReader):
    def __init__(self, code):
        super().__init__()
        self._code = code

    def get_next_character(self) -> str:
        character = self._code[self._position.character] if self._position.character < len(self._code) else EOF
        self.update_position(character)
        return character
