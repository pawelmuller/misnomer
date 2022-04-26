from lexer.dictionaries import ESCAPE_CHARACTERS, ONE_SIGN_TOKENS, DOUBLE_SIGN_TOKENS, DOUBLE_SIGN_TOKENS_PREFIXES, \
    KEYWORD_TOKENS, EOF, BACKSLASH
from lexer.lexer_exceptions import MisnomerLexerException, MisnomerLexerUnterminatedStringException
from lexer.token.token import Token
from lexer.token.token_type import TokenType
from utils.position import Position
from utils.source_reader import SourceReader

QUOTE_CHARACTERS = ("'", '"')


class Lexer:
    def __init__(self, reader: SourceReader):
        self._reader: SourceReader = reader
        self._current_character: str = ""
        self._position = Position()

    def get_next_character(self) -> str:
        """
        Method obtains and returns next character from the source reader.
        :return: string
        """
        next_character = self._reader.get_next_character()
        self._current_character = next_character
        self._position = self._reader.get_position()
        return next_character

    def omit_whitespaces(self) -> None:
        """
        Method that skips all whitespaces until it finds non-whitespace character
        """
        while self._current_character.isspace():
            self.get_next_character()

    def get_next_token(self):
        """
        Sth
        :return:
        """
        self.omit_whitespaces()
        self._position = self._reader.get_position()

        if token := self.get_simple_token():
            pass
        elif token := self.get_string_literal():
            pass
        elif token := self.get_number_literal():
            pass
        elif token := self.get_identifier_or_keyword():
            pass
        else:
            token = self.get_unknown_token()

        return token

    def get_simple_token(self):
        token_type = ONE_SIGN_TOKENS.get(self._current_character)

        if token_type in DOUBLE_SIGN_TOKENS_PREFIXES:
            buffer = self._current_character
            self.get_next_character()
            buffer += self._current_character
            if alternative_token_type := DOUBLE_SIGN_TOKENS.get(buffer):
                self.get_next_character()
                return Token(None, self._position, alternative_token_type)
        else:
            if token_type:
                self.get_next_character()
                return Token(None, self._position, token_type)

    def build_string(self):
        used_quote_sign = self._current_character
        buffer = ""
        self.get_next_character()

        while self._current_character != used_quote_sign:
            # EOF
            if self._current_character == EOF:
                raise MisnomerLexerUnterminatedStringException(self._position)
            # Escape characters
            elif self._current_character == BACKSLASH:
                self.get_next_character()
                if self._current_character == used_quote_sign:
                    buffer += used_quote_sign
                elif new_char := ESCAPE_CHARACTERS.get(BACKSLASH + self._current_character):
                    buffer += new_char
                else:
                    buffer += f"\\{self._current_character}"
            # Normal sign
            else:
                buffer += self._current_character
            self.get_next_character()

        return buffer

    def get_string_literal(self):
        if self._current_character in QUOTE_CHARACTERS:
            value = self.build_string()
            self.get_next_character()
            return Token(value, self._position, TokenType.STRING_LITERAL)

    def build_integer(self):
        if self._current_character.isdigit():
            value = ""
            while self._current_character.isdigit():
                value += self._current_character
                self.get_next_character()
            return value

    def get_number_literal(self):
        if value := self.build_integer():

            if value[:2] == '00':
                message = 'Failed building a number: expected "." but got "0" instead.'
                raise MisnomerLexerException(self._position, message)

            value = int(value)
            if self._current_character == '.':
                self.get_next_character()
                if fractional_part := self.build_integer():
                    fractional_part_digits_qty = len(fractional_part)
                    fractional_part = int(fractional_part) / (10 ** fractional_part_digits_qty)
                    value += fractional_part
                else:
                    message = f"Failed building a number: expected a digit after '.' got {self._current_character} instead."
                    raise MisnomerLexerException(self._position, message)

            return Token(value, self._position, TokenType.NUMERIC_LITERAL)

    def get_identifier_or_keyword(self):
        if self._current_character.isalpha():
            name = ""

            while self._current_character.isalpha() or self._current_character.isdigit() or self._current_character == '_':
                name += self._current_character
                self.get_next_character()

            if token_type := KEYWORD_TOKENS.get(name):
                name = None
            else:
                token_type = TokenType.IDENTIFIER

            return Token(name, self._position, token_type)

    def get_end_of_file_token(self):
        if self._current_character == EOF:
            token = Token(None, self._position, TokenType.EOF)
            self.get_next_character()
            return token

    def get_unknown_token(self):
        token = Token(self._current_character, self._position, TokenType.UNKNOWN)
        self.get_next_character()
        return token
