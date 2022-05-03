import pytest

from lexer.dictionaries import ONE_SIGN_TOKENS, DOUBLE_SIGN_TOKENS, KEYWORD_TOKENS
from lexer.lexer import Lexer
from lexer.lexer_exceptions import MisnomerLexerUnterminatedStringException, MisnomerLexerNumericBuildException
from lexer.token.token import Token
from lexer.token.token_type import TokenType
from utils.position import Position
from utils.source_reader.source_reader import StringSourceReader


class TestLexerTokenAssignments:
    def test_one_sign_tokens(self):
        tokens = ONE_SIGN_TOKENS.keys()
        for token in tokens:
            source = StringSourceReader(token)
            lexer_result = Lexer(source).get_next_token()

            assert lexer_result.get_type() == ONE_SIGN_TOKENS.get(token)

    def test_double_sign_tokens(self):
        tokens = DOUBLE_SIGN_TOKENS.keys()
        for token in tokens:
            source = StringSourceReader(token)
            lexer_result = Lexer(source).get_next_token()

            assert lexer_result.get_type() == DOUBLE_SIGN_TOKENS.get(token)

    def test_keyword_tokens(self):
        tokens = KEYWORD_TOKENS.keys()
        for token in tokens:
            source = StringSourceReader(token)
            lexer_result = Lexer(source).get_next_token()

            assert lexer_result.get_type() == KEYWORD_TOKENS.get(token)

    def test_function_code(self):
        function_code = """
            fibonacci(n: int) returns int {
                if (n <= 1) { return n; }
                else {
                    var a: int = fibonacci(n-1);
                    var b: int = fibonacci(n-2);
                    return a+b;
                }
            }
        """
        correct_tokens = [TokenType.IDENTIFIER, TokenType.ROUND_BRACKET_L, TokenType.IDENTIFIER, TokenType.COLON,
                          TokenType.INT, TokenType.ROUND_BRACKET_R, TokenType.RETURNS, TokenType.INT,
                          TokenType.CURLY_BRACKET_L, TokenType.IF, TokenType.ROUND_BRACKET_L, TokenType.IDENTIFIER,
                          TokenType.LESS_EQUAL, TokenType.NUMERIC_LITERAL, TokenType.ROUND_BRACKET_R,
                          TokenType.CURLY_BRACKET_L, TokenType.RETURN, TokenType.IDENTIFIER, TokenType.SEMICOLON,
                          TokenType.CURLY_BRACKET_R, TokenType.ELSE, TokenType.CURLY_BRACKET_L, TokenType.VAR,
                          TokenType.IDENTIFIER, TokenType.COLON, TokenType.INT, TokenType.ASSIGNMENT,
                          TokenType.IDENTIFIER, TokenType.ROUND_BRACKET_L, TokenType.IDENTIFIER, TokenType.SUBTRACT,
                          TokenType.NUMERIC_LITERAL, TokenType.ROUND_BRACKET_R, TokenType.SEMICOLON,
                          TokenType.VAR, TokenType.IDENTIFIER, TokenType.COLON, TokenType.INT, TokenType.ASSIGNMENT,
                          TokenType.IDENTIFIER, TokenType.ROUND_BRACKET_L, TokenType.IDENTIFIER, TokenType.SUBTRACT,
                          TokenType.NUMERIC_LITERAL, TokenType.ROUND_BRACKET_R, TokenType.SEMICOLON, TokenType.RETURN,
                          TokenType.IDENTIFIER, TokenType.ADD, TokenType.IDENTIFIER, TokenType.SEMICOLON,
                          TokenType.CURLY_BRACKET_R, TokenType.CURLY_BRACKET_R, TokenType.EOF]
        source = StringSourceReader(function_code)

        lexer = Lexer(source)
        tokens = []
        token = Token(None, Position(), TokenType.UNKNOWN)
        while token._type != TokenType.EOF:
            token = lexer.get_next_token()
            tokens.append(token.get_type())

        assert tokens == correct_tokens


class TestLexerExceptions:
    def test_non_escaped_string(self):
        code = "var a: string = 'Testing unterminated string;"

        source = StringSourceReader(code)
        lexer = Lexer(source)
        token = Token(None, Position(), TokenType.UNKNOWN)

        with pytest.raises(MisnomerLexerUnterminatedStringException):
            while token._type != TokenType.EOF:
                token = lexer.get_next_token()

    def test_double_zero_integer_beginning(self):
        code = "var a: int = 0012"

        source = StringSourceReader(code)
        lexer = Lexer(source)
        token = Token(None, Position(), TokenType.UNKNOWN)

        with pytest.raises(MisnomerLexerNumericBuildException):
            while token._type != TokenType.EOF:
                token = lexer.get_next_token()

    def test_double_zero_float_beginning(self):
        code = "var a: int = 00.12"

        source = StringSourceReader(code)
        lexer = Lexer(source)
        token = Token(None, Position(), TokenType.UNKNOWN)

        with pytest.raises(MisnomerLexerNumericBuildException):
            while token._type != TokenType.EOF:
                token = lexer.get_next_token()

    def test_wrong_char_after_dot(self):
        code = "var a: int = 00.x12"

        source = StringSourceReader(code)
        lexer = Lexer(source)
        token = Token(None, Position(), TokenType.UNKNOWN)

        with pytest.raises(MisnomerLexerNumericBuildException):
            while token._type != TokenType.EOF:
                token = lexer.get_next_token()
