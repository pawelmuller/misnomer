from copy import copy

from lexer.lexer import Lexer
from lexer.token.token import Token
from lexer.token.token_type import TokenType
from parser.dictionaries import TYPES, AVAILABLE_VAR_TYPES, AVAILABLE_FUNCTION_TYPES, \
    RELATIONAL_EXPRESSIONS, ADDITIVE_OPERATORS, MULTIPLICATIVE_OPERATORS
from parser.parser_exceptions import MisnomerParserUnexpectedTokenException, \
    MisnomerParserNoFunctionStatementBlockException, MisnomerParserNoElseStatementBlockException, \
    MisnomerParserNoIfConditionException, MisnomerParserNoWhileConditionException, \
    MisnomerParserNoExpressionException, MisnomerParserNoWhileInstructionsException, \
    MisnomerParserNoIfInstructionsException, MisnomerParserNoSecondRelationalExpressionException
from parser.syntax_tree.expressions import AndExpression, NotExpression, OrExpression, AdditiveExpression, \
    MultiplicativeExpression
from parser.syntax_tree.literals import NumericLiteral, StringLiteral
from parser.syntax_tree.statements import FunctionParameter, StatementBlock, IfStatement, FunctionDefinition, \
    Condition, WhileStatement, FunctionCall, Identifier, VariableInitialisationStatement, AssignmentStatement, \
    ReturnStatement, BreakStatement, ContinueStatement
from parser.syntax_tree.syntax_tree import Program


class Parser:
    def __init__(self, lexer: Lexer):
        self._lexer: Lexer = lexer
        self._current_token: Token = self._lexer.get_next_token()

    def get_current_token_position(self):
        return copy(self._current_token.get_position())

    def get_next_token(self):
        self._current_token = self._lexer.get_next_token()

    def consume_token(self, token_types: TokenType or [TokenType], *, strict: bool = False) -> Token:
        if isinstance(token_types, TokenType):
            token_types = [token_types]
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
            return_type = self.consume_token(AVAILABLE_FUNCTION_TYPES, strict=True)
            statement_block = self.parse_statement_block()

            if not statement_block:
                raise MisnomerParserNoFunctionStatementBlockException(function_name, self.get_current_token_position())

            return FunctionDefinition(function_name, function_parameters, TYPES.get(return_type.get_type()),
                                      statement_block, token.get_position())

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
            parameter_type = self.consume_token(AVAILABLE_VAR_TYPES, strict=True)
            parameter = FunctionParameter(identifier.get_value(), TYPES.get(parameter_type.get_type()),
                                          identifier.get_position())
            return parameter

    def parse_statement_block(self) -> StatementBlock:
        if token := self.consume_token(TokenType.CURLY_BRACKET_L, strict=False):
            statement_block = StatementBlock(token.get_position())

            while statement := self.parse_statement():
                statement_block.add_statement(statement)

            self.consume_token(TokenType.CURLY_BRACKET_R, strict=True)

            return statement_block

    def parse_statement(self):
        if statement := self.parse_statement_with_block():
            pass
        elif statement := self.parse_statement_without_block():
            pass
        return statement

    def parse_statement_with_block(self):
        if statement := self.parse_if_statement():
            pass
        elif statement := self.parse_while_statement():
            pass
        return statement

    def parse_statement_without_block(self):
        if statement := self.parse_variable_initialisation():
            pass
        elif statement := self.parse_identifier_statement():
            pass
        elif statement := self.parse_return_statement():
            pass
        elif statement := self.parse_loop_control_statement():
            pass

        if statement:
            self.consume_token(TokenType.SEMICOLON, strict=True)
            return statement

    def parse_if_statement(self) -> IfStatement:
        if token := self.consume_token(TokenType.IF, strict=False):
            condition = self.parse_condition(exception=MisnomerParserNoIfConditionException)
            if not (instructions := self.parse_conditional_instructions()):
                raise MisnomerParserNoIfInstructionsException(self.get_current_token_position())

            else_statement = None
            if self.consume_token(TokenType.ELSE, strict=False):
                if not (else_statement := self.parse_conditional_instructions()):
                    raise MisnomerParserNoElseStatementBlockException(self.get_current_token_position())

            return IfStatement(condition, instructions, else_statement, token.get_position())

    def parse_condition(self, exception):
        token = self.consume_token(TokenType.ROUND_BRACKET_L, strict=True)
        if not (logic_expression := self.parse_or_expression()):
            raise exception(self.get_current_token_position())
        self.consume_token(TokenType.ROUND_BRACKET_R, strict=True)

        return Condition(logic_expression, token.get_position())

    def parse_conditional_instructions(self):
        return self.parse_statement_block() or self.parse_statement()

    def parse_expression(self, parse_sub_expression, acceptable_connector, expression_class):
        if first_expression := parse_sub_expression():
            expressions = [first_expression]
            while self.consume_token(acceptable_connector, strict=False):
                if not (expression := parse_sub_expression()):
                    raise MisnomerParserNoExpressionException(self._current_token.get_type(),
                                                              self.get_current_token_position())
                expressions.append(expression)

            if len(expressions) == 1:
                return first_expression
            else:
                return expression_class(expressions, first_expression.get_position())

    def parse_or_expression(self):
        return self.parse_expression(self.parse_and_expression, TokenType.OR, OrExpression)

    def parse_and_expression(self) -> AndExpression:
        return self.parse_expression(self.parse_relational_expression, TokenType.AND, AndExpression)

    def parse_relational_expression(self):
        if first_expression := self.parse_additive_expression():
            if expression_operator := self.consume_token(RELATIONAL_EXPRESSIONS.keys(), strict=False):
                if not (second_expression := self.parse_additive_expression()):
                    raise MisnomerParserNoSecondRelationalExpressionException(self._current_token.get_type(),
                                                                              self.get_current_token_position())
                expression_class = RELATIONAL_EXPRESSIONS.get(expression_operator.get_type())
                return expression_class(first_expression, second_expression, first_expression.get_position())
            return first_expression

    def parse_additive_expression(self):
        if first_expression := self.parse_multiplicative_expression():
            expressions = [first_expression]
            while operator := self.consume_token(ADDITIVE_OPERATORS, strict=False):
                if not (expression := self.parse_multiplicative_expression()):
                    raise MisnomerParserNoExpressionException(self._current_token.get_type(),
                                                              self.get_current_token_position())
                if operator.get_type() == TokenType.SUBTRACT:
                    expression = NotExpression(expression, operator.get_position())

                expressions.append(expression)

            if len(expressions) == 1:
                return first_expression
            else:
                return AdditiveExpression(expressions, first_expression.get_position())

    def parse_multiplicative_expression(self):
        return self.parse_expression(self.parse_base_expression, MULTIPLICATIVE_OPERATORS, MultiplicativeExpression)

    def parse_base_expression(self):
        operator = self.consume_token(TokenType.SUBTRACT, strict=False) \
                   or self.consume_token(TokenType.NOT, strict=False)

        if expression := self.parse_parenthesized_operation():
            pass
        elif expression := self.parse_value():
            pass

        if operator:
            if not expression:
                raise MisnomerParserNoExpressionException(operator.get_type(), operator.get_position())
            return NotExpression(expression, operator.get_position())
        return expression

    def parse_parenthesized_operation(self):
        if self.consume_token(TokenType.ROUND_BRACKET_L, strict=False):
            logic_expression = self.parse_or_expression()
            self.consume_token(TokenType.ROUND_BRACKET_R, strict=True)
            return logic_expression

    def parse_value(self):
        if expression := self.parse_literal():
            pass
        elif expression := self.parse_identifier_expression():
            pass
        return expression

    def parse_literal(self):
        if literal := self.parse_numeric_literal():
            pass
        elif literal := self.parse_string_literal():
            pass
        return literal

    def parse_identifier_expression(self):
        if identifier := self.consume_token(TokenType.IDENTIFIER, strict=False):
            if expression := self._parse_function_call(identifier):
                pass
            else:
                expression = Identifier(identifier.get_value(), identifier.get_position())
            return expression

    def parse_numeric_literal(self):
        if token := self.consume_token(TokenType.NUMERIC_LITERAL, strict=False):
            return NumericLiteral(token.get_value(), token.get_position())

    def parse_string_literal(self):
        if token := self.consume_token(TokenType.STRING_LITERAL, strict=False):
            return StringLiteral(token.get_value(), token.get_position())

    def parse_not_expression(self) -> NotExpression:
        if token := self.consume_token(TokenType.NOT, strict=False):
            if not (logic_expression := self.parse_or_expression()):
                raise MisnomerParserNoExpressionException(self._current_token.get_type(),
                                                          self.get_current_token_position())
            return NotExpression(logic_expression, token.get_position())
        else:
            return self.parse_or_expression()

    def parse_while_statement(self):
        if token := self.consume_token(TokenType.WHILE, strict=False):
            condition = self.parse_condition(exception=MisnomerParserNoWhileConditionException)
            if not (instructions := self.parse_conditional_instructions()):
                raise MisnomerParserNoWhileInstructionsException(self.get_current_token_position())

            return WhileStatement(condition, instructions, token.get_position())

    def parse_variable_initialisation(self):
        if self.consume_token(TokenType.VAR, strict=False):
            identifier = self.consume_token(TokenType.IDENTIFIER, strict=True)
            self.consume_token(TokenType.COLON, strict=True)
            type_token = self.consume_token(AVAILABLE_VAR_TYPES, strict=True)
            variable_type = TYPES.get(type_token.get_type())
            if self.consume_token(TokenType.ASSIGNMENT, strict=False):
                if value := self.parse_or_expression():
                    return VariableInitialisationStatement(identifier.get_value(), value, variable_type,
                                                           identifier.get_position())
            return VariableInitialisationStatement(identifier.get_value(), None, variable_type,
                                                   identifier.get_position())

    def parse_identifier_statement(self):
        if identifier_token := self.consume_token(TokenType.IDENTIFIER, strict=False):
            if statement := self._parse_variable_assignment(identifier_token):
                pass
            elif statement := self._parse_function_call(identifier_token):
                pass
            return statement

    def _parse_variable_assignment(self, token):
        if self.consume_token(TokenType.ASSIGNMENT, strict=False):
            if value := self.parse_or_expression():
                return AssignmentStatement(token.get_value(), value, token.get_position())

    def parse_return_statement(self):
        if token := self.consume_token(TokenType.RETURN, strict=False):
            expression = self.parse_or_expression()

            return ReturnStatement(expression, token.get_position())

    def parse_loop_control_statement(self):
        if token := self.consume_token(TokenType.BREAK, strict=False):
            return BreakStatement(token.get_position())
        if token := self.consume_token(TokenType.CONTINUE, strict=False):
            return ContinueStatement(token.get_position())

    def _parse_function_call(self, token):
        if self.consume_token(TokenType.ROUND_BRACKET_L, strict=False):
            arguments = self.parse_call_arguments()
            self.consume_token(TokenType.ROUND_BRACKET_R, strict=True)

            return FunctionCall(token.get_value(), arguments, token.get_position())

    def parse_call_arguments(self):
        arguments = []
        if argument := self.parse_or_expression():
            arguments.append(argument)

            while token := self.consume_token(TokenType.COMA, strict=False) is not None:
                if (expression := self.parse_or_expression()) is None:
                    raise MisnomerParserNoExpressionException(token.get_type(), token.get_position())
                arguments.append(expression)

        return arguments
