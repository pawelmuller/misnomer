from parser.syntax_tree.syntax_tree import Node
from utils.position import Position


class Expression(Node):
    def __init__(self, expressions: list, position: Position):
        super().__init__(position)
        self.expressions = expressions


class LogicExpression(Expression):
    def __init__(self, expressions: list, position: Position):
        super().__init__(expressions, position)


class AndExpression(Expression):
    def __init__(self, expressions: list, position: Position):
        super().__init__(expressions, position)


class NotExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)


class MathematicalExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)


class MultiplicativeExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)


class BaseMathematicalExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)


class BinaryExpression(Node):  # Not sure about naming
    def __init__(self, left, right, position: Position):
        super().__init__(position)
        self.left = left
        self.right = right


class EqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)


class NotEqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)


class LessExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)


class LessEqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)


class GreaterExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)


class GreaterEqualExpression(BinaryExpression):
    def __init__(self, left, right, position: Position):
        super().__init__(left, right, position)
