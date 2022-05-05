from lexer.token.token_type import TokenType
from utils.position import Position


class Token:
    def __init__(self, value, position: Position, token_type: TokenType):
        self._value = value
        self._position = position
        self._type = token_type

    def __repr__(self):
        return f"Token {self._type.name} ({self._position}) = {self._value}"

    def get_type(self):
        return self._type
