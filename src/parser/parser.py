from copy import copy

from lexer.lexer import Lexer
from lexer.token.token import Token
from lexer.token.token_type import TokenType
from parser.parser_exceptions import MisnomerParserUnexpectedTokenException, MisnomerParserNoFunctionBodyException
from parser.syntax_tree import Program, FunctionDefinition, FunctionArgument, StatementBlock
from utils.position import Position

AVAILABLE_TYPES = (TokenType.INT, TokenType.FLOAT, TokenType.STRING)


class Parser:
    def __init__(self, lexer: Lexer):
        self._lexer: Lexer = lexer
        self._current_token: Token = self._lexer.get_next_token()
        self._position: Position = Position()

    def get_position(self):
        return copy(self._position)

    def get_next_token(self):
        self._current_token = self._lexer.get_next_token()

    def consume_token(self, token_type: TokenType, *, strict: bool = False) -> Token:
        return self.consume_tokens([token_type], strict=strict)

    def consume_tokens(self, token_types: [TokenType], *, strict: bool = False) -> Token:
        token = self._current_token
        if token.get_type() in token_types:
            self.get_next_token()
            return token
        elif strict:
            raise MisnomerParserUnexpectedTokenException(token_types, self._current_token.get_type(),
                                                         self.get_position())

    def parse_program(self) -> Program:
        program = Program(self._position)
        while function_definition := self.parse_function_definition():
            program.add_function_definition(function_definition)

        return program

    def parse_function_definition(self) -> FunctionDefinition:
        if token := self.consume_token(TokenType.IDENTIFIER, strict=False):
            function_name = token.get_value()
            self.consume_token(TokenType.ROUND_BRACKET_L, strict=True)
            function_arguments = self.parse_arguments()
            self.consume_token(TokenType.ROUND_BRACKET_R, strict=True)
            self.consume_token(TokenType.RETURNS, strict=True)
            return_type = self.consume_tokens(AVAILABLE_TYPES, strict=True)
            statement_block = self.parse_statement_block()

            if not statement_block:
                raise MisnomerParserNoFunctionBodyException(function_name, self.get_position())

            return FunctionDefinition(function_name, function_arguments, return_type, statement_block,
                                      self.get_position())

    def parse_arguments(self) -> [FunctionArgument]:
        arguments = []

        if first_argument := self.consume_token(TokenType.IDENTIFIER, strict=False):
            self.consume_token(TokenType.COLON, strict=True)
            argument_type = self.consume_tokens(AVAILABLE_TYPES, strict=True)
            argument = FunctionArgument(first_argument.get_value(), argument_type)
            arguments.append(argument)

            while self.consume_token(TokenType.COMA, strict=False):
                token = self.consume_token(TokenType.IDENTIFIER, strict=True)
                self.consume_token(TokenType.COLON, strict=True)
                argument_type = self.consume_tokens(AVAILABLE_TYPES, strict=True)
                argument = FunctionArgument(token.get_value(), argument_type)
                arguments.append(argument)

            return arguments

    def parse_statement_block(self) -> StatementBlock:
        if self.consume_token(TokenType.CURLY_BRACKET_L, strict=False):
            statement_block = StatementBlock(self.get_position())

            while statement := self.parse_statement():
                statement_block.add_statement(statement)

            self.consume_token(TokenType.CURLY_BRACKET_R, strict=True)

            return statement_block

    def parse_statement(self):
        if statement := self.parse_if_statement():
            return statement
        if statement := self.parse_while_statement():
            return statement
        if statement := self.parse_return_statement():
            return statement
        if statement := self.parse_function_call():
            return statement
        if statement := self.parse_variable_initialisation():
            return statement
        if statement := self.parse_loop_control():
            return statement

    def parse_if_statement(self):
        pass

    def parse_while_statement(self):
        pass

    def parse_return_statement(self):
        pass

    def parse_function_call(self):
        pass

    def parse_variable_initialisation(self):
        pass

    def parse_loop_control(self):
        pass

