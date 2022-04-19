from enum import Enum, auto


class TokenType(Enum):
    # Statements
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    RETURN = auto()

    # Base operators
    ASSIGNMENT = auto()

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
    PLUS = auto()               # +
    MINUS = auto()              # -
    MULTIPLY = auto()           # *
    DIVIDE = auto()             # /
