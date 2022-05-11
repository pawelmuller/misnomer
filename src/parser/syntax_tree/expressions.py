from parser.syntax_tree.syntax_tree import Node
from utils.position import Position


class Expression(Node):
    def __init__(self, expressions: list, position: Position):
        super().__init__(position)
        self.expressions = expressions


class OrExpression(Expression):
    def __init__(self, expressions: list, position: Position):
        super().__init__(expressions, position)


class AndExpression(Expression):
    def __init__(self, expressions: list, position: Position):
        super().__init__(expressions, position)


class NotExpression(Expression):
    def __init__(self, expressions, position: Position):
        super().__init__(expressions, position)
