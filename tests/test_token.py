import pytest

from lexer.token.exceptions import MisnomerTokenInappropriateTypeException
from lexer.token.token import Token
from lexer.token.token_type import TokenType
from utils.position import Position


class TestToken:
    def test_simple_token(self):
        token = Token(None, Position(1, 1, 1), TokenType.COLON)

        assert token.get_type() == TokenType.COLON
        assert token.get_position() == Position(1, 1, 1)
        assert token.get_value() is None

    def test_simple_token_with_value(self):
        token = Token("Something", Position(1, 1, 1), TokenType.STRING_LITERAL)

        assert token.get_type() == TokenType.STRING_LITERAL
        assert token.get_position() == Position(1, 1, 1)
        assert token.get_value() == "Something"

    def test_token_value_and_type_check(self):
        with pytest.raises(MisnomerTokenInappropriateTypeException):
            Token("Something", Position(1, 1, 1), TokenType.NUMERIC_LITERAL)

    def test_token_value_and_type_check_2(self):
        with pytest.raises(MisnomerTokenInappropriateTypeException):
            Token(155, Position(1, 1, 1), TokenType.STRING_LITERAL)

    def test_token_value_and_type_check_3(self):
        with pytest.raises(MisnomerTokenInappropriateTypeException):
            Token(155.3746, Position(1, 1, 1), TokenType.STRING_LITERAL)

    def test_token_value_and_type_check_4(self):
        with pytest.raises(MisnomerTokenInappropriateTypeException):
            Token(155.3746, Position(1, 1, 1), TokenType.COLON)

