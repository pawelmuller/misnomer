from interpreter.builtin_functions import builtin_functions
from interpreter.interpreter_exceptions import MisnomerInterpreterExceededMaximumDepthException


class Context:
    def __init__(self, recursion_limit, available_calls):
        self.functions = builtin_functions.copy()
        self.variables = {}
        self._recursion_limit = recursion_limit
        self._available_calls = available_calls
        if available_calls <= 0:
            raise MisnomerInterpreterExceededMaximumDepthException(recursion_limit)

    def add_function(self, function_name, function):
        self.functions[function_name] = function

    def get_function(self, function_name):
        return self.functions.get(function_name)

    def add_variable(self, variable_name, variable_value):
        self.variables[variable_name] = variable_value

    def get_variable(self, name):
        return self.variables.get(name)

    def get_context_copy(self):
        new_context = Context(self._recursion_limit, self._available_calls-1)
        new_context.functions = self.functions
        return new_context


class Interpreter:
    def __init__(self, program, recursion_limit=1000):
        self.program = program
        self.context = Context(recursion_limit, recursion_limit)

    def execute(self):
        exit_code = self.program.execute(self.context)
        return exit_code
