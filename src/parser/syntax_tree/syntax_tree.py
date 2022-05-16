from copy import copy

from utils.position import Position


class Node:
    def __init__(self, position: Position):
        self.position = position

    def __repr__(self):
        return self.__class__.__name__

    def get_position(self):
        return copy(self.position)


class Program(Node):
    def __init__(self):
        super().__init__(Position())
        self.function_definitions = []

    def add_function_definition(self, function_definition):
        self.function_definitions.append(function_definition)
