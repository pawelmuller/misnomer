from interpreter.builtin_functions import builtin_functions
from interpreter.interpreter_exceptions import MisnomerInterpreterExceededMaximumDepthException


class Context:
    recursion_limit = 0

    def __init__(self, available_calls):
        self.functions = builtin_functions.copy()
        self.variables = {}
        self._available_calls = available_calls
        if available_calls <= 0:
            raise MisnomerInterpreterExceededMaximumDepthException(Context.recursion_limit)
        self._return_flag = False

    def add_function(self, function_name, function):
        self.functions[function_name] = function

    def get_function(self, function_name):
        return self.functions.get(function_name)

    def set_variable(self, variable_name, variable_value):
        self.variables[variable_name] = variable_value

    def get_variable(self, name):
        return self.variables.get(name)

    def get_new_context(self):
        new_context = Context(self._available_calls - 1)
        new_context.functions = self.functions
        return new_context

    def set_return_flag(self, new_value: bool):
        self._return_flag = new_value

    def get_return_flag(self):
        return self._return_flag


class Interpreter:
    def __init__(self, program, recursion_limit=1000):
        self.program = program
        self.context = Context(recursion_limit)
        Context.recursion_limit = recursion_limit

    def execute(self):
        exit_code = self.program.execute(self.context)
        return exit_code
