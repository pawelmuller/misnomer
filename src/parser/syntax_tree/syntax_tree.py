from utils.position import Position


class Node:
    def __init__(self, position: Position):
        self.position = position

    def __repr__(self):
        return self.__class__.__name__


class Program(Node):
    def __init__(self):
        super().__init__(Position())

    def add_function_definition(self, function_definition):
        pass
