from copy import copy
from io import TextIOWrapper, BytesIO
from typing import IO

from lexer.dictionaries import EOF
from utils.exceptions.exceptions import MisnomerExecutiveNotFoundError, MisnomerEncodingError
from utils.position import Position


class SourceReader:
    _END_OF_LINE = "\n"

    def __init__(self, source):
        self._source = source
        self._position = Position()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._source.close()

    def update_position(self, character: str):
        """
        Updates position depending on character kind.

        :param character: Determines what component of position should be updated
        """
        if character == SourceReader._END_OF_LINE:
            self._position.line += 1
            self._position.column = 0
        else:
            self._position.column += 1

        self._position.character += 1

    def get_first_character(self) -> str:
        """
        Obtains one character from source without updating position (since default is correct).

        :return: string
        """
        character = self._source.read(1)
        if not character:
            character = EOF
        return character

    def get_next_character(self) -> str:
        """
        Obtains one character from source.

        :return: string
        """
        character = self._source.read(1)
        if not character:
            character = EOF
        self.update_position(character)
        return character

    def get_position(self) -> Position:
        """
        Returns a copy of position reader is currently at.

        :return: Copy of reader position
        """
        return copy(self._position)


class FileSourceReader(SourceReader):
    def __init__(self, source_path: str):
        self._source_path: str = source_path
        source = self._load_source()
        super().__init__(source)

    def _load_source(self) -> IO:
        """
        Loads contents of the file at given source_path.

        :return: IO containing contents of the file at given source_path
        """
        try:
            source = open(self._source_path, "r", encoding="utf-8")
            return source
        except FileNotFoundError:
            raise MisnomerExecutiveNotFoundError(self._source_path)
        except ValueError or UnicodeDecodeError as error:
            raise MisnomerEncodingError(error)


class StringSourceReader(SourceReader):
    def __init__(self, code):
        input_bytes = BytesIO(code.encode('utf-8'))
        source = TextIOWrapper(input_bytes, encoding='utf-8')
        super().__init__(source)
