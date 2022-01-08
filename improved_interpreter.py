INTEGER, MUL, DIV, PLUS, MINUS, EOF = 'INTEGER', 'MUL', 'DIV', 'PLUS', 'MINUS', 'EOF'


class Token:
    def __init__(self, value, type) -> None:
        self.value = value
        if value.isnumeric():
            self.value = int(self.value)
        self.type = type

    def __str__(self) -> str:
        return f'Token({self.value}, {self.type})'


class Lexer:
    def __init__(self, code):
        self.code = code.replace(' ', '')
        self.curchar: str = None
        self.curpos = 0

    def advance(self):
        if not self.curpos >= len(self.code):
            self.curchar = self.code[self.curpos]
        self.curpos += 1

    def get_next_token(self):
        self.advance()
        if self.curpos > len(self.code):
            return Token('EOF', EOF)

        if self.curchar.isnumeric():
            return Token(self.curchar, INTEGER)

        if self.curchar == '+':
            return Token(self.curchar, PLUS)

        if self.curchar == '-':
            return Token(self.curchar, MINUS)

        if self.curchar == '*':
            return Token(self.curchar, MUL)

        if self.curchar == '/':
            return Token(self.curchar, DIV)


class Interpreter:
    def __init__(self, lexer) -> None:
        self.lexer: Lexer = lexer
        self.curtoken = None

    def factor(self):
        processed_value = self.lexer.get_next_token()
        self.curtoken = processed_value
        print(self.curtoken)
        return processed_value.value

    def term(self):
        result = self.factor()

        self.factor()
        while self.curtoken.type in (MUL, DIV):
            if self.curtoken.type == MUL:
                result *= self.factor()
            if self.curtoken.type == DIV:
                result //= self.factor()
            self.factor()
        return result

    def expr(self):
        result = self.term()

        while self.curtoken.type in (PLUS, MINUS):
            if self.curtoken.type == MINUS:
                result -= self.term()

            if self.curtoken.type == PLUS:
                result += self.term()
        return result


if __name__ == '__main__':
    while True:
        expression = input('calc> ')
        lexer = Lexer(expression)

        interpreter = Interpreter(lexer)
        result = interpreter.expr()
        print(result)
