from lexer.token.token_type import TokenType
from utils.position import Position


class Token:
    def __init__(self, value, position: Position, token_type: TokenType):
        self._value = value
        self._position = position
        self._type = token_type

    def __repr__(self):
        return f"Token {self._type.name} ({self._position}) = {self._value}"

    def __eq__(self, other):
        if self._value == other.get_value() and self._position == other.get_position() and self._type == other.get_type():
            return True
        return False

    def get_value(self):
        return self._value

    def get_type(self):
        return self._type

    def get_position(self):
        return self._position
