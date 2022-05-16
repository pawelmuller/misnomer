from parser.syntax_tree.syntax_tree import Node
from parser.types import Type
from utils.position import Position


class Statement(Node):
    def __init__(self, position: Position):
        super().__init__(position)


class StatementBlock(Node):
    def __init__(self, position: Position):
        super().__init__(position)
        self.statements = []

    def add_statement(self, statement):
        self.statements.append(statement)

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.statements == other.statements


class FunctionParameter(Node):
    def __init__(self, name: str, argument_type: Type, position: Position):
        super().__init__(position)
        self.name = name
        self.argument_type = argument_type

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.name == other.name and self.argument_type == other.argument_type


class FunctionDefinition(Node):
    def __init__(self, name: str, arguments: [FunctionParameter], return_type: Type, statement_block: StatementBlock,
                 position: Position):
        super().__init__(position)
        self.name = name
        self.arguments = arguments
        self.return_type = return_type
        self.statement_block = statement_block

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq_1 = self.name == other.name and self.arguments == other.arguments
        attributes_eq_2 = self.return_type == other.return_type and self.statement_block == other.statement_block
        return super_eq and attributes_eq_1 and attributes_eq_2


class FunctionCall(Node):
    def __init__(self, identifier, arguments, position: Position):
        super().__init__(position)
        self.identifier = identifier
        self.arguments = arguments

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq = self.identifier == other.identifier and self.arguments == other.arguments
        return super_eq and attributes_eq


class Identifier(Node):
    def __init__(self, name, position: Position):
        super().__init__(position)
        self.name = name

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.name == other.name


class Condition(Node):
    def __init__(self, logic_expression, position: Position):
        super().__init__(position)
        self.expression = logic_expression

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.expression == other.expression


class ConditionalStatement(Statement):
    def __init__(self, condition: Condition, instructions, position: Position):
        super().__init__(position)
        self.condition = condition
        self.instructions = instructions

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq = self.condition == other.condition and self.instructions == other.instructions
        return super_eq and attributes_eq


class IfStatement(ConditionalStatement):
    def __init__(self, condition: Condition, instructions, else_statement, position: Position):
        super().__init__(condition, instructions, position)
        self.else_statement = else_statement

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq = self.else_statement == other.else_statement
        return super_eq and attributes_eq


class WhileStatement(ConditionalStatement):
    def __init__(self, condition: Condition, instructions, position: Position):
        super().__init__(condition, instructions, position)


class ReturnStatement(Node):
    def __init__(self, value, position: Position):
        super().__init__(position)
        self.value = value

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.value == other.value


class VariableInitialisationStatement(Statement):
    def __init__(self, name, value, variable_type: Type, position: Position):
        super().__init__(position)
        self.name = name
        self.value = value
        self.variable_type = variable_type

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq_1 = self.name == other.name and self.value == other.value
        attributes_eq_2 = self.variable_type == other.variable_type
        return super_eq and attributes_eq_1 and attributes_eq_2


class AssignmentStatement(Statement):
    def __init__(self, name, value, position: Position):
        super().__init__(position)
        self.name = name
        self.value = value

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq = self.name == other.name and self.value == other.value
        return super_eq and attributes_eq


class BreakStatement(Statement):
    def __init__(self, position: Position):
        super().__init__(position)


class ContinueStatement(Statement):
    def __init__(self, position: Position):
        super().__init__(position)
