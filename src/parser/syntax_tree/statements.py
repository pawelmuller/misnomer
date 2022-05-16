from parser.syntax_tree.syntax_tree import Node
from parser.types import Type
from utils.position import Position


class Statement(Node):
    def __init__(self, position: Position):
        super().__init__(position)


class StatementBlock(Node):
    def __init__(self, position: Position):
        super().__init__(position)

    def add_statement(self, statement):
        pass


class FunctionParameter(Node):
    def __init__(self, name: str, argument_type: Type, position: Position):
        super().__init__(position)
        self.name = name
        self.argument_type = argument_type


class FunctionDefinition(Node):
    def __init__(self, name: str, arguments: [FunctionParameter], return_type: Type, statement_block: StatementBlock,
                 position: Position):
        super().__init__(position)
        self.name = name
        self.arguments = arguments
        self.return_type = return_type
        self.statement_block = statement_block


class FunctionCall(Node):
    def __init__(self, identifier, arguments, position: Position):
        super().__init__(position)
        self.identifier = identifier
        self.arguments = arguments


class Identifier(Node):
    def __init__(self, name, position: Position):
        super().__init__(position)
        self.name = name


class Condition(Node):
    def __init__(self, logic_expression, position: Position):
        super().__init__(position)


class IfStatement(Statement):
    def __init__(self, condition: Condition, instructions, else_statement, position: Position):
        super().__init__(position)
        self.condition = condition
        self.instructions = instructions
        self.else_statement = else_statement


class WhileStatement(Statement):
    def __init__(self, condition: Condition, instructions, position: Position):
        super().__init__(position)
        self.condition = condition
        self.instructions = instructions


class ReturnStatement(Node):
    def __init__(self, value, position: Position):
        super().__init__(position)
        self.value = value


class VariableInitialisationStatement(Statement):
    def __init__(self, name, value, position: Position):
        super().__init__(position)
        self.name = name
        self.value = value


class AssignmentStatement(Statement):
    def __init__(self, name, value, position: Position):
        super().__init__(position)
        self.name = name
        self.value = value

