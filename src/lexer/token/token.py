from lexer import TokenType


class Token:
    def __init__(self, value, line: int, column: int, token_type: TokenType):
        self._value = value
        self._line = line
        self._column = column
        self._type = token_type

    def __repr__(self):
        return f"Token {self._type.name} (l: {self._line} c: {self._column}) = {self._value}"
