from copy import copy
from io import TextIOWrapper, BytesIO

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
        if character == SourceReader._END_OF_LINE:
            self._position.line += 1
            self._position.column = 0
        else:
            self._position.column += 1

        self._position.character += 1

    def get_next_character(self) -> str:
        character = self._source.read(1)
        if not character:
            character = EOF
        self.update_position(character)
        return character

    def get_position(self):
        return copy(self._position)


class FileSourceReader(SourceReader):
    def __init__(self, source_path: str):
        source = self._load_source()
        super().__init__(source)
        self._source_path: str = source_path
        self._source: TextIOWrapper

    def _load_source(self):
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
