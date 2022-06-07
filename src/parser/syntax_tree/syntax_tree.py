from copy import copy

from interpreter.interpreter_exceptions import MisnomerInterpreterNoMainFunctionException
from parser.parser_exceptions import MisnomerParserFunctionNameDuplicateException
from utils.position import Position


class Node:
    def __init__(self, position: Position):
        self.position = position

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.position}"

    def get_position(self):
        return copy(self.position)

    def execute(self, context):
        raise NotImplemented("This is just an interface method.")

    def __eq__(self, other):
        return self.position == other.position


class Program(Node):
    def __init__(self):
        super().__init__(Position())
        self.function_definitions: dict = {}

    def add_function_definition(self, function_definition):
        function_name = function_definition.get_name()
        if function_name in self.function_definitions:
            raise MisnomerParserFunctionNameDuplicateException(function_name, function_definition.get_position())
        self.function_definitions[function_name] = function_definition

    def execute(self, context):
        for function_name, function in self.function_definitions.items():
            function.execute(context)
        if main := context.functions.get("main"):
            if (exit_code := main.statement_block.execute(context)) is not None:
                return exit_code
            return 0
        raise MisnomerInterpreterNoMainFunctionException(self.position)

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.function_definitions == other.function_definitions
