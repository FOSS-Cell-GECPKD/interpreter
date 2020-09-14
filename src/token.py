class Token:
    def __init__(self, type, lexeme, literal, line):
        """
        type: type of the token
        lexeme: raw substring of the source code
        literal: actual value of lexeme
        line: line number of occurance
        """
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        if self.literal is None:
            return f"<{self.type} '{self.lexeme}' >"
        else:
            return f"<{self.type} '{self.lexeme}' {self.literal} >"
