class Interpreter:
    def __init__(self, program):
        self.program = program

    def execute(self):
        exit_code = self.program.execute()
        return exit_code
