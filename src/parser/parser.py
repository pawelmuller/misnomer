from copy import copy

from lexer.lexer import Lexer
from lexer.token.token import Token
from lexer.token.token_type import TokenType
from parser.parser_exceptions import MisnomerParserUnexpectedTokenException, \
    MisnomerParserNoFunctionStatementBlockException, MisnomerParserNoElseStatementBlockException, \
    MisnomerParserNoIfConditionException, MisnomerParserNoWhileConditionException, MisnomerParserNoExpressionException
from parser.syntax_tree.expressions import AndExpression, NotExpression, OrExpression
from parser.syntax_tree.statements import FunctionParameter, StatementBlock, IfStatement, IfCondition, WhileCondition, \
    FunctionDefinition
from parser.syntax_tree.syntax_tree import Program

AVAILABLE_TYPES = (TokenType.INT, TokenType.FLOAT, TokenType.STRING)


class Parser:
    def __init__(self, lexer: Lexer):
        self._lexer: Lexer = lexer
        self._current_token: Token = self._lexer.get_next_token()

    def get_current_token_position(self):
        return copy(self._current_token.get_position())

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
                                                         self.get_current_token_position())

    def parse_program(self) -> Program:
        program = Program()
        while function_definition := self.parse_function_definition():
            program.add_function_definition(function_definition)

        return program

    def parse_function_definition(self) -> FunctionDefinition:
        if token := self.consume_token(TokenType.IDENTIFIER, strict=False):
            function_name = token.get_value()
            self.consume_token(TokenType.ROUND_BRACKET_L, strict=True)
            function_parameters = self.parse_parameters()
            self.consume_token(TokenType.ROUND_BRACKET_R, strict=True)
            self.consume_token(TokenType.RETURNS, strict=True)
            return_type = self.consume_tokens(AVAILABLE_TYPES, strict=True)
            statement_block = self.parse_statement_block()

            if not statement_block:
                raise MisnomerParserNoFunctionStatementBlockException(function_name, self.get_current_token_position())

            return FunctionDefinition(function_name, function_parameters, TYPES.get(return_type.get_type()),
                                      statement_block, self.get_current_token_position())

    def parse_parameters(self) -> [FunctionParameter]:
        parameters = []

        if first_parameter := self.parse_parameter(strict=False):
            parameters.append(first_parameter)

            while self.consume_token(TokenType.COMA, strict=False):
                parameter = self.parse_parameter(strict=True)
                parameters.append(parameter)

            return parameters

    def parse_parameter(self, *, strict: bool = False) -> FunctionParameter:
        if identifier := self.consume_token(TokenType.IDENTIFIER, strict=strict):
            self.consume_token(TokenType.COLON, strict=True)
            parameter_type = self.consume_tokens(AVAILABLE_TYPES, strict=True)
            parameter = FunctionParameter(identifier.get_value(), TYPES.get(parameter_type.get_type()),
                                          self.get_current_token_position())
            return parameter

    def parse_statement_block(self) -> StatementBlock:
        if self.consume_token(TokenType.CURLY_BRACKET_L, strict=False):
            statement_block = StatementBlock(self.get_current_token_position())

            while statement := self.parse_statement():
                statement_block.add_statement(statement)

            self.consume_token(TokenType.CURLY_BRACKET_R, strict=True)

            return statement_block

    def parse_statement(self):
        if statement := self.parse_variable_initialisation():
            return statement
        if statement := self.parse_if_statement():
            return statement
        if statement := self.parse_while_statement():
            return statement
        if statement := self.parse_return_statement():
            return statement
        if statement := self.parse_loop_control():
            return statement
        if statement := self.parse_function_call():
            return statement

    def parse_if_statement(self) -> IfStatement:
        if self.consume_token(TokenType.IF, strict=False):
            if_condition = self.parse_if_condition()
            if_statement_block = self.parse_statement_block()

            else_statement = None
            if self.consume_token(TokenType.ELSE, strict=False):
                if else_statement := self.parse_if_statement():
                    pass
                elif else_statement := self.parse_statement_block():
                    pass
                else:
                    raise MisnomerParserNoElseStatementBlockException(self.get_current_token_position())

            return IfStatement(if_condition, if_statement_block, else_statement, self.get_current_token_position())

    def parse_while_condition(self) -> WhileCondition:
        return self.parse_condition(TokenType.WHILE, WhileCondition, MisnomerParserNoWhileConditionException)

    def parse_if_condition(self):
        return self.parse_condition(TokenType.IF, IfCondition, MisnomerParserNoIfConditionException)

    def parse_condition(self, token_type, condition_class,
                        exception: MisnomerParserNoWhileConditionException or MisnomerParserNoIfConditionException):
        if self.consume_token(token_type, strict=False):
            self.consume_token(TokenType.OPEN_PARENTHESIS, strict=True)
            if not (operation := self.parse_or_expression()):
                raise exception(self.get_current_token_position())
            self.consume_token(TokenType.CLOSING_PARENTHESIS, strict=True)

            return condition_class(operation)

    def parse_or_expression(self):
        if first_expression := self.parse_and_expression():
            expressions = [first_expression]
            while self.consume_token(TokenType.OR, strict=False):
                if not (expression := self.parse_and_expression()):
                    raise MisnomerParserNoExpressionException(self._current_token.get_type(),
                                                              self.get_current_token_position())
                expressions.append(expression)

            if len(expressions) == 1:
                return first_expression
            else:
                return OrExpression(expressions, self.get_current_token_position())

    def parse_and_expression(self) -> AndExpression:
        if first_expression := self.parse_not_expression():
            expressions = [first_expression]
            while self.consume_token(TokenType.AND, strict=False):
                if not (expression := self.parse_not_expression()):
                    raise MisnomerParserNoExpressionException(self._current_token.get_type(),
                                                              self.get_current_token_position())
                expressions.append(expression)

            if len(expressions) == 1:
                return first_expression
            else:
                return AndExpression(expressions, self.get_current_token_position())

    def parse_not_expression(self) -> NotExpression:
        if self.consume_token(TokenType.NOT, strict=False):
            if not (logic_expression := self.parse_logic_expression()):
                raise MisnomerParserNoExpressionException(self._current_token.get_type(),
                                                          self.get_current_token_position())
            return NotExpression(logic_expression, self.get_current_token_position())
        else:
            return self.parse_logic_expression()

    def parse_logic_expression(self):
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
