INTEGER, PLUS, MINUS, EOF = 'INTEGER', 'PLUS', 'MINUS', 'EOF'
MUL, DIV, LPAREN, RPAREN = 'MUL', 'DIV', 'LPAREN', 'RPAREN'


class Token:
    def __init__(self, value, type) -> None:
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return f'Token({self.value}, {self.type})'


class Lexer:
    def __init__(self, code: str) -> None:
        self.code = code.replace(' ', '')
        self.curpos = 0
        self.curchar: str = None

    def advance(self):
        if self.curpos >= len(self.code):
            return
        self.curchar = self.code[self.curpos]
        self.curpos += 1

    def get_next_token(self):
        self.advance()
        if self.curpos > len(self.code):
            return Token('EOF', EOF)

        if self.curchar.isnumeric():
            return Token(int(self.curchar), INTEGER)

        elif self.curchar == '+':
            return Token('+', PLUS)

        elif self.curchar == '-':
            return Token('-', MINUS)

        elif self.curchar == '/':
            return Token('/', DIV)

        elif self.curchar == '*':
            return Token('*', MUL)

        elif self.curchar == '(':
            return Token('(', LPAREN)

        elif self.curchar == ')':
            return Token(')', RPAREN)


class IntegerNode:
    def __init__(self, token) -> None:
        self.value = token.value
        self.token = token

    def __str__(self) -> str:
        return f'IntegerNode({self.token})'


class OperandNode:
    def __init__(self, left, op, right) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f'OperandNode({self.left}, {self.op}, {self.right})'


class Parser:
    def __init__(self, lexer) -> None:
        self.lexer: Lexer = lexer
        self.curtoken = self.lexer.get_next_token()

    def advance(self):
        token = self.lexer.get_next_token()
        self.curtoken = token

    def factor(self):
        if self.curtoken.type == INTEGER:
            node = IntegerNode(self.curtoken)
            self.advance()
        if self.curtoken.type == LPAREN:
            self.advance()
            node = self.expr()
            self.advance()
        return node

    def term(self):
        node = self.factor()

        while self.curtoken.type in (MUL, DIV):
            op = self.curtoken
            self.advance()
            node = OperandNode(node, op, self.factor())
        return node

    def expr(self):
        node = self.term()

        while self.curtoken.type in (PLUS, MINUS):
            op = self.curtoken
            self.advance()
            node = OperandNode(node, op, self.term())
        return node


class SyntaxTreeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise NotImplementedError(f"No visit method for {type(node).__name__}")


class InfixToPostfixTranslator(SyntaxTreeVisitor):
    def __init__(self, parser: Parser) -> None:
        self.parser = parser

    def visit_OperandNode(self, node: OperandNode):
        right = self.visit(node.right)
        left = self.visit(node.left)

        return f'{left} {right} {node.op.value}'

    def visit_IntegerNode(self, node: IntegerNode):
        return node.value

    def translate(self):
        tree = self.parser.expr()
        return self.visit(tree)


if __name__ == '__main__':
    while True:
        code = input('code> ')
        lexer = Lexer(code)
        parser = Parser(lexer)
        visitor = InfixToPostfixTranslator(parser)
        result = visitor.translate()
        print(result)
