from enum import Enum, auto


class TokenType(Enum):
    # Statements
    IF = auto()                 # if
    ELSE = auto()               # else
    WHILE = auto()              # while
    RETURN = auto()             # return
    RETURNS = auto()            # returns
    VAR = auto()                # var

    # Identifier
    IDENTIFIER = auto()

    # Types
    INT = auto()                # int
    FLOAT = auto()              # float
    STRING = auto()             # string
    NOTHING = auto()            # nothing

    # Base operators
    ASSIGNMENT = auto()         # =

    AND = auto()                # and or &&
    OR = auto()                 # or or ||

    EQUAL = auto()              # ==
    NOT_EQUAL = auto()          # !=
    LESS = auto()               # <
    LESS_EQUAL = auto()         # <=
    GREATER = auto()            # >
    GREATER_EQUAL = auto()      # >=

    NOT = auto()                # not or !

    # Mathematical
    ADD = auto()                # +
    SUBTRACT = auto()           # -
    MULTIPLY = auto()           # *
    DIVIDE = auto()             # /

    # Special characters
    ROUND_BRACKET_L = auto()    # (
    ROUND_BRACKET_R = auto()    # )
    CURLY_BRACKET_L = auto()    # {
    CURLY_BRACKET_R = auto()    # }
    DOT = auto()                # .
    COMA = auto()               # ,
    COLON = auto()              # :
    SEMICOLON = auto()          # ;
    DOUBLE_QUOTES = auto()      # "

    # Remaining
    UNKNOWN = auto()


