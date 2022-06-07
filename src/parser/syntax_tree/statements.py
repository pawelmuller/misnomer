from interpreter.dictionaries import misnomer_types_to_python_types
from interpreter.interpreter_exceptions import MisnomerInterpreterVariableAlreadyExistsException, \
    MisnomerInterpreterArgumentsNumberDoesNotMatchException, MisnomerInterpreterFunctionDoesNotExistException, \
    MisnomerInterpreterVariableDoesNotExistException, MisnomerInterpreterCastingException, \
    MisnomerInterpreterCastingBuiltinException, MisnomerInterpreterVariableAssignmentTypeException, \
    MisnomerInterpreterFunctionReturnTypeException
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

    def execute(self, context):
        for statement in self.statements:
            if (exit_code := statement.execute(context)) is not None:
                return exit_code

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.statements == other.statements

    def __repr__(self):
        return super().__repr__() + ":" + " ".join([str(node) for node in self.statements])


class FunctionParameter(Node):
    def __init__(self, name: str, argument_type: Type, position: Position):
        super().__init__(position)
        self.name = name
        self.argument_type = argument_type

    def get_name(self):
        return self.name

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

    def get_name(self):
        return self.name

    def check_if_value_matches_type(self, result):
        value_type = type(result)
        if correct_types := misnomer_types_to_python_types.get(self.return_type):
            if value_type not in correct_types:
                raise MisnomerInterpreterFunctionReturnTypeException(value_type, self.return_type.name,
                                                                     self.name, self.position)

    def execute(self, context):
        if self.name in context.functions:
            raise MisnomerInterpreterVariableAlreadyExistsException(self.name, self.position)
        context.add_function(self.name, self)

    def __call__(self, context, *call_arguments_values):
        if (got_arguments_number := len(call_arguments_values)) != (expected_arguments_number := len(self.arguments)):
            raise MisnomerInterpreterArgumentsNumberDoesNotMatchException(expected_arguments_number,
                                                                          got_arguments_number,
                                                                          self.name, self.position)
        new_context = context.get_context_copy()
        for argument_name, argument_value in zip(self.arguments, call_arguments_values):
            new_context.add_variable(argument_name, argument_value)
        result = self.statement_block.execute(new_context)
        self.check_if_value_matches_type(result)
        return result

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

    def execute(self, context):
        arguments = [argument.execute(context) for argument in self.arguments]

        if function := context.get_function(self.identifier):
            if isinstance(function, FunctionDefinition):
                arguments = [context] + arguments
            try:
                return function(*arguments)
            except MisnomerInterpreterCastingBuiltinException as e:
                raise MisnomerInterpreterCastingException(e.cast_type, e.expression, self.position)
        else:
            raise MisnomerInterpreterFunctionDoesNotExistException(self.identifier, self.position)

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq = self.identifier == other.identifier and self.arguments == other.arguments
        return super_eq and attributes_eq


class Identifier(Node):
    def __init__(self, name, position: Position):
        super().__init__(position)
        self.name = name

    def execute(self, context):
        if (variable := context.get_variable(self.name)) is not None:
            return variable
        raise MisnomerInterpreterVariableDoesNotExistException(self.name, self.position)

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.name == other.name


class Condition(Node):
    def __init__(self, logic_expression, position: Position):
        super().__init__(position)
        self.expression = logic_expression

    def execute(self, context):
        return self.expression.execute(context)

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

    def execute(self, context):
        if self.condition.execute(context):
            return self.instructions.execute(context)
        elif self.else_statement:
            return self.else_statement.execute(context)

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        attributes_eq = self.else_statement == other.else_statement
        return super_eq and attributes_eq


class WhileStatement(ConditionalStatement):
    def __init__(self, condition: Condition, instructions, position: Position):
        super().__init__(condition, instructions, position)

    def execute(self, context):
        while self.condition.execute(context):
            if (exit_code := self.instructions.execute(context)) is not None:
                return exit_code


class ReturnStatement(Node):
    def __init__(self, value, position: Position):
        super().__init__(position)
        self.value = value

    def execute(self, context):
        return self.value.execute(context) if self.value is not None else None

    def __eq__(self, other):
        super_eq = super().__eq__(other)
        return super_eq and self.value == other.value


class VariableInitialisationStatement(Statement):
    def __init__(self, name, value, variable_type: Type, position: Position):
        super().__init__(position)
        self.name = name
        self.value = value
        self.variable_type = variable_type

    def check_if_value_matches_type(self, result):
        value_type = type(result)
        if correct_types := misnomer_types_to_python_types.get(self.variable_type):
            if value_type not in correct_types:
                raise MisnomerInterpreterVariableAssignmentTypeException(value_type, self.variable_type.name,
                                                                         self.name, self.position)

    def execute(self, context):
        if self.name in context.variables:
            raise MisnomerInterpreterVariableAlreadyExistsException(self.name, self.position)
        result = self.value.execute(context)
        self.check_if_value_matches_type(result)
        context.add_variable(self.name, result)

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

    def execute(self, context):
        if self.name not in context.variables:
            raise MisnomerInterpreterVariableDoesNotExistException(self.name, self.position)
        result = self.value.execute(context)
        variable_type = type(context.get_variable(self.name))
        if type(result) == variable_type:
            context.add_variable(self.name, result)
        else:
            raise MisnomerInterpreterVariableAssignmentTypeException(type(result), variable_type, self.name, self.position)

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
