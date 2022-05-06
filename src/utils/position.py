class Position:
    def __init__(self, line=1, column=1, character=1):
        self.line = line
        self.column = column
        self.character = character

    def __repr__(self):
        return f"l: {self.line}, c: {self.column}"
        # return f"l: {self.line}, c: {self.column}, ch: {self.character}"

    def __eq__(self, other):
        if self.line == other.line and self.column == other.column and self.character == other.character:
            return True
        return False
