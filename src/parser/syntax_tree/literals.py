from parser.syntax_tree.syntax_tree import Node
from utils.position import Position


class Literal(Node):
    def __init__(self, value, position: Position):
        super().__init__(position)
        self.value = value


class NumericLiteral(Literal):
    def __init__(self, value, position: Position):
        super().__init__(value, position)


class StringLiteral(Literal):
    def __init__(self, value, position: Position):
        super().__init__(value, position)
