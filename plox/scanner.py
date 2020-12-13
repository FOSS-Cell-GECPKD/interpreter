from plox.token import Token
from plox.token_type import TokenType


class Scanner:
    '''
    FLex/Lox or regex can be used to simplify this part
    But as our goal is to understand how things work,
    we can go the hand-crafting scanner
    '''

    start = 0
    current = 0
    line = 0

    tokens = []

    keywords = {
        'and': TokenType.AND,
        'class': TokenType.CLASS,
        'else': TokenType.ELSE,
        'false': TokenType.FALSE,
        'fun': TokenType.FUN,
        'for': TokenType.FOR,
        'if': TokenType.IF,
        'nil': TokenType.NIL,
        'or': TokenType.OR,
        'print': TokenType.PRINT,
        'return': TokenType.RETURN,
        'super': TokenType.SUPER,
        'this': TokenType.THIS,
        'true': TokenType.TRUE,
        'var': TokenType.VAR,
        'while': TokenType.WHILE,
    }

    def __init__(self, source):
        '''
        source: source code to be scanned
        '''
        self.source = source

    def scan_tokens(self):
        '''
        loop `scan_token` to find all the tokens
        in the source code
        '''
        # scan till the end of the source code
        while(not self.isend()):
            # beginning of the next lexeme
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        '''
        scan and returns a single token
        '''
        c = self.advance()
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)

        # handling one/two characters token
        elif c == '!':
            if self.match('='):
                self.add_token(TokenType.BANG_EQUAL)
            else:
                self.add_token(TokenType.BANG)
        elif c == '=':
            if self.match('='):
                self.add_token(TokenType.EQUAL_EQUAL)
            else:
                self.add_token(TokenType.EQUAL)
        elif c == '>':
            if self.match('='):
                self.add_token(TokenType.GREATER_EQUAL)
            else:
                self.add_token(TokenType.GREATER)
        elif c == '<':
            if self.match('='):
                self.add_token(TokenType.LESSER_EQUAL)
            else:
                self.add_token(TokenType.LESSER)
        elif c == '/':
            # comment starts with //
            # ignore the comment
            if self.match('/'):
                while (self.peek() != '\n') and (not self.isend()):
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)

        # skip the meaningless characters
        elif (c == ' ') | (c == '\t') | (c == '\r'):
            pass
        elif c == '\n':
            self.line += 1

        # Literal
        elif c == '"':
            self.string()

        elif c.isdigit():
            self.number()

        elif (c.isalpha()) or (c == '_'):
            self.identifier()

        else:
            # TODO: pythonic error
            # self.error(self.line, 'unexpected character')
            print("error")

    def identifier(self):
        c = self.peek()
        while (c.isalnum()) or (c == '_'):
            self.advance()
            c = self.peek()

        # check if the identifier is a reserved word
        text = self.source[self.start:self.current]

        type = self.keywords.get(text, None)
        if type is None:
            type = TokenType.IDENTIFIER
        self.add_token(type)

    def number(self):
        '''
        Extracts the integer/floating point literal
        from the source code
        '''
        c = self.peek()
        while c.isdigit():
            self.advance()
            c = self.peek()

        # look for the fractional part.
        c = self.peek_next()
        if (self.peek() == '.') and c.isdigit():
            # consume the "."
            self.advance()

            c = self.peek()
            while c.isdigit():
                self.advance()
                c = self.peek()

        self.add_token(TokenType.NUMBER, int(self.source[self.start:self.current]))

    def string(self):
        '''
        Extracts the sting literal from
        the source code
        '''
        while (self.peek() != '"') and (not self.isend()):
            # multiline string are possible
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        # unterminated string
        if self.isend():
            # TODO: Proper error
            print(f"{self.line} Unterminated string.")
            return

        # closing
        self.advance()

        # trim the surrounding qoutes
        value = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, value)

    def isend(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current-1]

    def add_token(self, type, literal=None):
        # TODO: verify
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected):
        '''
        Only consumes the value if it matches
        '''
        if self.isend():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        '''
        return the next char without consuming it
        '''
        if self.isend():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        '''
        here we purposefully created peek() and peek_next()
        The only required look ahead is 1,2.
        '''
        if (self.current+1 >= len(self.source)):
            return '\0'
        return self.source[self.current+1]
