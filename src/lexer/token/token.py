from lexer.token.exceptions import MisnomerTokenInappropriateTypeException
from lexer.token.token_type import TokenType
from utils.position import Position

correct_types_for_values: dict[type, tuple[TokenType]] = {
    str: (TokenType.STRING_LITERAL, TokenType.IDENTIFIER),
    int: (TokenType.NUMERIC_LITERAL, ),
    float: (TokenType.NUMERIC_LITERAL, ),
}


class Token:
    def __init__(self, value, position: Position, token_type: TokenType):
        self._value = value
        self._position = position
        self._type = token_type
        self.check_if_type_matches_value()

    def __repr__(self):
        return f"Token {self._type.name} ({self._position}) = {self._value}"

    def get_type(self) -> TokenType:
        return self._type

    def get_position(self) -> Position:
        return self._position

    def get_value(self) -> int or float or str:
        return self._value

    def check_if_type_matches_value(self):
        if self._type == TokenType.UNKNOWN:
            return
        if self._value is not None:
            if correct_types := correct_types_for_values.get(type(self._value)):
                if self._type not in correct_types:
                    raise MisnomerTokenInappropriateTypeException(type(self._value), self._type, self._position)
