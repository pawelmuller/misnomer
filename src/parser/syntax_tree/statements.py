from parser.syntax_tree.syntax_tree import Node
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
    def __init__(self, name: str, argument_type, position: Position):
        super().__init__(position)
        self.name = name
        self.argument_type = argument_type


class FunctionDefinition(Node):
    def __init__(self, name: str, arguments: [FunctionParameter], return_type, statement_block: StatementBlock,
                 position: Position):
        super().__init__(position)
        self.name = name
        self.arguments = arguments
        self.return_type = return_type
        self.statement_block = statement_block


class IfCondition(Node):
    def __init__(self, position: Position):
        super().__init__(position)


class IfStatement(Statement):
    def __init__(self, condition: IfCondition, statement_block: StatementBlock, else_statement, position: Position):
        super().__init__(position)
        self.condition = condition
        self.statement_block = statement_block
        self.else_statement = "" if else_statement is None else else_statement


class WhileCondition(Node):
    def __init__(self, position: Position):
        super().__init__(position)


class WhileStatement(Statement):
    def __init__(self, condition: WhileCondition, statement_block: StatementBlock, position: Position):
        super().__init__(position)
        self.condition = condition
        self.scope = statement_block


class ReturnStatement(Node):
    def __init__(self, value, position: Position):
        super().__init__(position)
        self.value = value