builtin_functions = {
    "print": print,
    "input": input,
}


class Context:
    def __init__(self):
        self.functions = builtin_functions.copy()
        self.variables = {}


class Interpreter:
    def __init__(self, program):
        self.program = program
        self.context = Context()

    def execute(self):
        exit_code = self.program.execute(self.context)
        return exit_code
