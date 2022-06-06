from lexer.token.token_type import TokenType
from parser.syntax_tree.expressions import EqualExpression, NotEqualExpression, LessExpression, LessEqualExpression, \
    GreaterExpression, GreaterEqualExpression
from parser.types import Type

AVAILABLE_VAR_TYPES = (TokenType.INT, TokenType.FLOAT, TokenType.STRING)
AVAILABLE_FUNCTION_TYPES = AVAILABLE_VAR_TYPES + (TokenType.NOTHING, )

TYPES = {
    TokenType.INT: Type.INT,
    TokenType.FLOAT: Type.FLOAT,
    TokenType.STRING: Type.STRING,
    TokenType.NOTHING: Type.NOTHING
}

RELATIONAL_EXPRESSIONS = {
    TokenType.EQUAL: EqualExpression,
    TokenType.NOT_EQUAL: NotEqualExpression,
    TokenType.LESS: LessExpression,
    TokenType.LESS_EQUAL: LessEqualExpression,
    TokenType.GREATER: GreaterExpression,
    TokenType.GREATER_EQUAL: GreaterEqualExpression
}

ADDITIVE_OPERATORS = (TokenType.ADD, TokenType.SUBTRACT)

MULTIPLICATIVE_OPERATORS = (TokenType.MULTIPLY, TokenType.DIVIDE)
