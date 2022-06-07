from interpreter.builtin_functions import builtin_functions


class Context:
    def __init__(self):
        self.functions = builtin_functions.copy()
        self.variables = {}

    def add_function(self, function_name, function):
        self.functions[function_name] = function

    def get_function(self, function_name):
        return self.functions.get(function_name)

    def add_variable(self, variable_name, variable_value):
        self.variables[variable_name] = variable_value

    def get_variable(self, name):
        return self.variables.get(name)

    def get_context_copy(self):
        new_context = Context()
        new_context.functions = self.functions
        return new_context


class Interpreter:
    def __init__(self, program):
        self.program = program
        self.context = Context()

    def execute(self):
        exit_code = self.program.execute(self.context)
        return exit_code
