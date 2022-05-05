class Position:
    def __init__(self, line=0, column=0, character=0):
        self.line = line
        self.column = column
        self.character = character

    def __repr__(self):
        return f"l: {self.line}, c: {self.column}"
