from copy import copy

from utils.position import Position


class Node:
    def __init__(self, position: Position):
        self.position = position

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.position}"

    def get_position(self):
        return copy(self.position)

    def __eq__(self, other):
        return self.position == other.position


class Program(Node):
    def __init__(self):
        super().__init__(Position())
        self.function_definitions = []

    def add_function_definition(self, function_definition):
        self.function_definitions.append(function_definition)

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.function_definitions == other.function_definitions

