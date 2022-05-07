from utils.position import Position


class Node:
    pass


class SyntaxTree:
    pass


class FunctionArgument:
    def __init__(self, name: str, argument_type):
        self.name = name
        self.argument_type = argument_type


class FunctionBody:
    def __init__(self, position: Position):
        self.position: Position = position


class FunctionDefinition:
    def __init__(self, name: str, arguments: [FunctionArgument], return_type, body: list, position: Position):
        self.name = name
        self.arguments = arguments
        self.return_type = return_type
        self.body = body
        self.position: Position = position


class Program:
    def __init__(self, position: Position):
        self._position: Position = position

    def add_function_definition(self, function_definition: FunctionDefinition):
        pass
