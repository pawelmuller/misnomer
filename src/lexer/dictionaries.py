from lexer.token.token_type import TokenType

EOF = "\0"
BACKSLASH = "\\"


ONE_SIGN_TOKENS = {
    "=": TokenType.ASSIGNMENT,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
    "!": TokenType.NOT,
    "+": TokenType.ADD,
    "-": TokenType.SUBTRACT,
    "*": TokenType.MULTIPLY,
    "/": TokenType.DIVIDE,
    "(": TokenType.ROUND_BRACKET_L,
    ")": TokenType.ROUND_BRACKET_R,
    "{": TokenType.CURLY_BRACKET_L,
    "}": TokenType.CURLY_BRACKET_R,
    ",": TokenType.COMA,
    ":": TokenType.COLON,
    ";": TokenType.SEMICOLON,
    EOF: TokenType.EOF
}

DOUBLE_SIGN_TOKENS_PREFIXES = (
    TokenType.ASSIGNMENT,
    TokenType.LESS,
    TokenType.GREATER,
    TokenType.NOT
)

DOUBLE_SIGN_TOKENS = {
    "==": TokenType.EQUAL,
    "!=": TokenType.NOT_EQUAL,
    "<=": TokenType.LESS_EQUAL,
    ">=": TokenType.GREATER_EQUAL
}

KEYWORD_TOKENS = {
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "while": TokenType.WHILE,
    "return": TokenType.RETURN,
    "returns": TokenType.RETURNS,
    "var": TokenType.VAR,
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "string": TokenType.STRING,
    "nothing": TokenType.NOTHING,
    "or": TokenType.OR,
    "and": TokenType.AND,
    "not": TokenType.NOT
}

ESCAPE_CHARACTERS = {
    "n": "\n",        # New line
    "r": "\r",        # Carriage return
    "t": "\t",        # Tab
    "b": "\b",        # Backspace
    "f": "\f",        # Form feed
    "\\": BACKSLASH,  # Backslash
    "0": EOF          # EOF
}
