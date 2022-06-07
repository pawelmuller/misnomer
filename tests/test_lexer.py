import pytest

from lexer.dictionaries import ONE_SIGN_TOKENS, DOUBLE_SIGN_TOKENS, KEYWORD_TOKENS
from lexer.lexer import Lexer
from lexer.lexer_exceptions import MisnomerLexerUnterminatedStringException, MisnomerLexerNumericBuildException, \
    MisnomerLexerStringBuildExceededLengthException
from lexer.token.token import Token
from lexer.token.token_type import TokenType
from utils.position import Position
from utils.source_reader.source_reader import StringSourceReader


class TestLexerTokenAssignments:
    def test_one_sign_tokens(self):
        tokens = ONE_SIGN_TOKENS.keys()
        for token in tokens:
            with StringSourceReader(token) as source:
                lexer_result = Lexer(source).get_next_token()

            assert lexer_result.get_type() == ONE_SIGN_TOKENS.get(token)

    def test_double_sign_tokens(self):
        tokens = DOUBLE_SIGN_TOKENS.keys()
        for token in tokens:
            with StringSourceReader(token) as source:
                lexer_result = Lexer(source).get_next_token()

            assert lexer_result.get_type() == DOUBLE_SIGN_TOKENS.get(token)

    def test_keyword_tokens(self):
        tokens = KEYWORD_TOKENS.keys()
        for token in tokens:
            with StringSourceReader(token) as source:
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
                while(1) {
                    continue;
                    break;
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
                          TokenType.CURLY_BRACKET_R, TokenType.WHILE, TokenType.ROUND_BRACKET_L,
                          TokenType.NUMERIC_LITERAL, TokenType.ROUND_BRACKET_R, TokenType.CURLY_BRACKET_L,
                          TokenType.CONTINUE, TokenType.SEMICOLON, TokenType.BREAK, TokenType.SEMICOLON,
                          TokenType.CURLY_BRACKET_R, TokenType.CURLY_BRACKET_R, TokenType.EOF]

        with StringSourceReader(function_code) as source:
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

        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            token = Token(None, Position(), TokenType.UNKNOWN)

            with pytest.raises(MisnomerLexerUnterminatedStringException):
                while token._type != TokenType.EOF:
                    token = lexer.get_next_token()

    def test_too_long_string(self):
        code = f"var a: string = '{'s'*1001}'"

        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            token = Token(None, Position(), TokenType.UNKNOWN)

            with pytest.raises(MisnomerLexerStringBuildExceededLengthException):
                while token._type != TokenType.EOF:
                    token = lexer.get_next_token()

    def test_double_zero_integer_beginning(self):
        code = "var a: int = 0012"

        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            token = Token(None, Position(), TokenType.UNKNOWN)

            with pytest.raises(MisnomerLexerNumericBuildException):
                while token._type != TokenType.EOF:
                    token = lexer.get_next_token()

    def test_double_zero_float_beginning(self):
        code = "var a: int = 00.12"

        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            token = Token(None, Position(), TokenType.UNKNOWN)

            with pytest.raises(MisnomerLexerNumericBuildException):
                while token._type != TokenType.EOF:
                    token = lexer.get_next_token()

    def test_wrong_char_after_dot(self):
        code = "var a: int = 00.x12"

        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            token = Token(None, Position(), TokenType.UNKNOWN)

            with pytest.raises(MisnomerLexerNumericBuildException):
                while token._type != TokenType.EOF:
                    token = lexer.get_next_token()

    def test_no_char_after_dot(self):
        code = "var a: int = 00."

        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            token = Token(None, Position(), TokenType.UNKNOWN)

            with pytest.raises(MisnomerLexerNumericBuildException):
                while token._type != TokenType.EOF:
                    token = lexer.get_next_token()

    def test_maximum_string_length(self):
        code = "var a: string = 'Something longer than anticipated';"

        with StringSourceReader(code) as source:
            lexer = Lexer(source, 20)
            token = Token(None, Position(), TokenType.UNKNOWN)

            with pytest.raises(MisnomerLexerStringBuildExceededLengthException):
                while token._type != TokenType.EOF:
                    token = lexer.get_next_token()


class TestPosition:
    def test_position_after_example_function(self):
        function_code = """fibonacci(n: int) returns int {
    if (n <= 1) { return n; }
    else {
        var a: int = fibonacci(n-1);
        var b: int = fibonacci(n-2);
        return a+b;
    }
}"""

        correct_positions = [Position(1, 1, 1), Position(1, 10, 10), Position(1, 11, 11), Position(1, 12, 12),
                             Position(1, 14, 14), Position(1, 17, 17), Position(1, 19, 19), Position(1, 27, 27),
                             Position(1, 31, 31), Position(2, 5, 37), Position(2, 8, 40), Position(2, 9, 41),
                             Position(2, 11, 43), Position(2, 14, 46), Position(2, 15, 47), Position(2, 17, 49),
                             Position(2, 19, 51), Position(2, 26, 58), Position(2, 27, 59), Position(2, 29, 61),
                             Position(3, 5, 67), Position(3, 10, 72), Position(4, 9, 82), Position(4, 13, 86),
                             Position(4, 14, 87), Position(4, 16, 89), Position(4, 20, 93), Position(4, 22, 95),
                             Position(4, 31, 104), Position(4, 32, 105), Position(4, 33, 106), Position(4, 34, 107),
                             Position(4, 35, 108), Position(4, 36, 109), Position(5, 9, 119), Position(5, 13, 123),
                             Position(5, 14, 124), Position(5, 16, 126), Position(5, 20, 130), Position(5, 22, 132),
                             Position(5, 31, 141), Position(5, 32, 142), Position(5, 33, 143), Position(5, 34, 144),
                             Position(5, 35, 145), Position(5, 36, 146), Position(6, 9, 156), Position(6, 16, 163),
                             Position(6, 17, 164), Position(6, 18, 165), Position(6, 19, 166), Position(7, 5, 172),
                             Position(8, 1, 174)]

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            token_positions = []
            while (token := lexer.get_next_token()).get_type() != TokenType.EOF:
                token_positions.append(token.get_position())

        assert token_positions == correct_positions
