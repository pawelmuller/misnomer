import pytest

from lexer.lexer import Lexer
from parser.parser import Parser
from parser.parser_exceptions import MisnomerParserUnexpectedTokenException, \
    MisnomerParserNoFunctionStatementBlockException, MisnomerParserFunctionNameDuplicateException, \
    MisnomerParserFunctionParameterNameDuplicateException
from parser.syntax_tree.expressions import EqualExpression, NotEqualExpression, NotExpression, GreaterEqualExpression, \
    OrExpression, AndExpression, AdditiveExpression, MultiplicativeExpression, MultiplicativeInvertedExpression, \
    AdditiveInvertedExpression
from parser.syntax_tree.literals import NumericLiteral
from parser.syntax_tree.statements import IfStatement, Condition, Identifier, ReturnStatement, StatementBlock, \
    FunctionCall, WhileStatement, AssignmentStatement, VariableInitialisationStatement
from parser.types import Type
from utils.position import Position
from utils.source_reader.source_reader import StringSourceReader


class TestParser:
    def test_if_statement_1(self):
        function_code = "if (something == something_different) return x;"
        correct_statement = IfStatement(
            condition=Condition(
                EqualExpression(
                    Identifier("something", Position(1, 5, 5)),
                    Identifier("something_different", Position(1, 18, 18)),
                    Position(1, 5, 5)
                ),
                Position(1, 4, 4)
            ),
            instructions=ReturnStatement(Identifier("x", Position(1, 46, 46)), Position(1, 39, 39)),
            else_statement=None,
            position=Position(1, 1, 1)
        )

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            statement = parser.parse_statement()

        assert statement == correct_statement

    def test_if_statement_2(self):
        function_code = "if (something != -2) { return x; } else { fibonacci(something); }"
        else_statement_block = StatementBlock(Position(1, 41, 41))
        else_statement_block.add_statement(
            FunctionCall(
                identifier="fibonacci",
                arguments=[Identifier("something", Position(1, 53, 53))],
                position=Position(1, 43, 43),
            ))
        instructions_statement_block = StatementBlock(Position(1, 22, 22))
        instructions_statement_block.add_statement(
            ReturnStatement(Identifier("x", Position(1, 31, 31)), Position(1, 24, 24))
        )
        correct_statement = IfStatement(
            condition=Condition(
                NotEqualExpression(
                    Identifier("something", Position(1, 5, 5)),
                    AdditiveInvertedExpression(
                        NumericLiteral(2, Position(1, 19, 19)),
                        Position(1, 18, 18)
                    ),
                    Position(1, 5, 5)
                ),
                Position(1, 4, 4)
            ),
            instructions=instructions_statement_block,
            else_statement=else_statement_block,
            position=Position(1, 1, 1)
        )

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            statement = parser.parse_statement()

        assert statement == correct_statement

    def test_complex_condition(self):
        function_code = "if (something != -2 and sth() and oth() or 1 == 2) { return; }"
        instructions_statement_block = StatementBlock(Position(1, 52, 52))
        instructions_statement_block.add_statement(
            ReturnStatement(None, Position(1, 54, 54))
        )
        correct_statement = IfStatement(
            condition=Condition(
                OrExpression([
                    AndExpression([
                        NotEqualExpression(
                            Identifier("something", Position(1, 5, 5)),
                            NotExpression(NumericLiteral(2, Position(1, 19, 19)), Position(1, 18, 18)),
                            Position(1, 5, 5)
                        ),
                        FunctionCall("sth", [], Position(1, 25, 25)),
                        FunctionCall("oth", [], Position(1, 35, 35))
                    ], Position(1, 5, 5)),
                    EqualExpression(NumericLiteral(1, Position(1, 44, 44)), NumericLiteral(2, Position(1, 49, 49)),
                                    Position(1, 44, 44))], Position(1, 5, 5)
                ), Position(1, 4, 4)
            ),
            instructions=instructions_statement_block,
            else_statement=None,
            position=Position(1, 1, 1)
        )

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            statement = parser.parse_statement()

        assert statement == correct_statement

    def test_complex_addition(self):
        function_code = "var a: int = 2 + 2 * 2 + 2;"

        correct_statement = VariableInitialisationStatement(
            name="a",
            position=Position(1, 1, 1),
            variable_type=Type.INT,
            value=AdditiveExpression(
                [
                    NumericLiteral(2, Position(1, 14, 14)),
                    MultiplicativeExpression([
                        NumericLiteral(2, Position(1, 18, 18)),
                        NumericLiteral(2, Position(1, 22, 22)),
                    ], Position(1, 18, 18)),
                    NumericLiteral(2, Position(1, 26, 26))
                ],
                Position(1, 14, 14)
            )
        )

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            statement = parser.parse_statement()

        assert statement == correct_statement

    def test_complex_multiplication(self):
        function_code = "var a: int = 2 * 2 * 2 + 2;"

        correct_statement = VariableInitialisationStatement(
            name="a",
            position=Position(1, 1, 1),
            variable_type=Type.INT,
            value=AdditiveExpression(
                [
                    MultiplicativeExpression([
                        NumericLiteral(2, Position(1, 14, 14)),
                        NumericLiteral(2, Position(1, 18, 18)),
                        NumericLiteral(2, Position(1, 22, 22)),
                    ], Position(1, 14, 14)),
                    NumericLiteral(2, Position(1, 26, 26))
                ],
                Position(1, 14, 14)
            )
        )

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            statement = parser.parse_statement()

        assert statement == correct_statement

    def test_while_statement(self):
        function_code = "while (something >= -9.2) { x = 10; }"

        instructions_statement_block = StatementBlock(Position(1, 27, 27))
        instructions_statement_block.add_statement(
            AssignmentStatement("x", NumericLiteral(10, Position(1, 33, 33)), Position(1, 29, 29)),
        )
        correct_statement = WhileStatement(
            condition=Condition(
                GreaterEqualExpression(
                    Identifier("something", Position(1, 8, 8)),
                    NotExpression(
                        NumericLiteral(9.2, Position(1, 22, 22)),
                        Position(1, 21, 21)
                    ),
                    Position(1, 8, 8)
                ),
                Position(1, 7, 7)
            ),
            instructions=instructions_statement_block,
            position=Position(1, 1, 1)
        )

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            statement = parser.parse_statement()

        assert statement == correct_statement

    def test_inverted_statements(self):
        function_code = "var a: int = ! 1 - 1 / sth() * 20 and 100;"

        correct_statement = VariableInitialisationStatement(
            name="a",
            position=Position(1, 1, 1),
            variable_type=Type.INT,
            value=AndExpression(
                expressions=[
                    AdditiveInvertedExpression(
                        AdditiveExpression([
                            NotExpression([NumericLiteral(1, Position(1, 16, 16))], Position(1, 14, 14)),
                            MultiplicativeExpression([
                                AdditiveInvertedExpression(
                                    NumericLiteral(1, Position(1, 20, 20)),
                                    Position(1, 20, 20)
                                ),
                                MultiplicativeInvertedExpression(
                                    FunctionCall(arguments=[], identifier="sth", position=Position(1, 24, 24)),
                                    Position(1, 20, 20)),
                                NumericLiteral(20, Position(1, 32, 32))
                            ], Position(1, 20, 20)),
                        ], Position(1, 14, 14)), Position(1, 18, 18)),
                    NumericLiteral(100, Position(1, 39, 39))
                ], position=Position(1, 14, 14)
            )
        )

        with StringSourceReader(function_code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            statement = parser.parse_statement()

        assert statement == correct_statement


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

    def test_function_name_duplication(self):
        code = """
            fibonacci(n: int) returns int {
                return;
            }
            fibonacci(n: int) returns int {
                return;
            }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserFunctionNameDuplicateException):
                parser.parse_program()

    def test_function_parameter_duplication(self):
        code = """
            fibonacci(n: int, n: string) returns int {
                return;
            }
        """
        with StringSourceReader(code) as source:
            lexer = Lexer(source)
            parser = Parser(lexer)

            with pytest.raises(MisnomerParserFunctionParameterNameDuplicateException):
                parser.parse_program()
