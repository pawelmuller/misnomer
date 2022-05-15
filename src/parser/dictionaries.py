from lexer.token.token_type import TokenType
from parser.types import Type

TYPES = {
    TokenType.INT: Type.INT,
    TokenType.FLOAT: Type.FLOAT,
    TokenType.STRING: Type.STRING,
    TokenType.NOTHING: Type.NOTHING
}
