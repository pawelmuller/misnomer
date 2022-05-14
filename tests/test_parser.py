import pytest

from lexer.lexer import Lexer
from parser.parser import Parser
from parser.parser_exceptions import MisnomerParserUnexpectedTokenException, \
    MisnomerParserNoFunctionStatementBlockException, MisnomerParserNoIfStatementBlockException
from utils.source_reader.source_reader import StringSourceReader


class TestParser:
    def test_one(self):
        assert 1 == 1


class TestParserExceptions:
    def test_unexpected_token_1(self):
        function_code = "fibonacci(n: int) returns var"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_unexpected_token_2(self):
        function_code = "fibonacci''(n: int)"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_unexpected_token_3(self):
        function_code = "fibonacci3.14(n: int)"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_unexpected_token_4(self):
        function_code = "fibonacci (n: int,)"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_unexpected_token_5(self):
        function_code = "fibonacci (n: int, x)"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_unexpected_token_6(self):
        function_code = "fibonacci (n: int, x:)"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_unexpected_token_7(self):
        function_code = "fibonacci (n: int, x: float)"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_unexpected_token_8(self):
        function_code = "fibonacci (n: int, x: float) returns"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserUnexpectedTokenException):
                parser.parse_program()

    def test_no_function_body_1(self):
        function_code = "fibonacci (n: int, x: float) returns int"

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserNoFunctionStatementBlockException):
                parser.parse_program()

    # def test_no_if_statement_block_1(self):
    #     function_code = "if (something == nothing)"
    #
    #     with StringSourceReader(function_code) as source:
    #         lexer = Lexer(source)
    #         parser = Parser(lexer)
    #
    #         with pytest.raises(MisnomerParserNoIfStatementBlockException):
    #             parser.parse_program()
