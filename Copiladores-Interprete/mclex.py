#mclex.py
from rich import print
import sly

class Lexer(sly.Lexer):
    tokens = {
        VOID, BOOL, INT, FLOAT, WHILE, IF, ELSE, RETURN, NEW, SIZE,
        CONTINUE, BREAK, AND, OR, EQ, NE, LE, GE, BOOL_LIT, INT_LIT,
        FLOAT_LIT, STRING_LIT, IDENT,
    }
    

    literals = '+-*/%=()[]{}<>.,;'
    ignore = r' \t\r'

    @_(r'//.*\n')
    def ignore_linecomment(self, t):
        self.lineno += 1

    @_(r'/\*(.|\n)*?\*/')
    def ignore_blockcomment(self, t):
        self.lineno += t.value.count('\n')

    @_(r'if')
    def IF(self, t):
        return t

    @_(r'else')
    def ELSE(self, t):
        return t

    @_(r'while')
    def WHILE(self, t):
        return t

    @_(r'return')
    def RETURN(self, t):
        return t

    @_(r'continue')
    def CONTINUE(self, t):
        return t

    @_(r'break')
    def BREAK(self, t):
        return t

    @_(r'new')
    def NEW(self, t):
        return t

    @_(r'void')
    def VOID(self, t):
        return t

    @_(r'bool')
    def BOOL(self, t):
        return t

    @_(r'int')
    def INT(self, t):
        return t

    @_(r'float')
    def FLOAT(self, t):
        return t

    @_(r'\d+\.\d+')
    def FLOAT_LIT(self, t):
        t.value = float(t.value)
        return t

    @_(r'\d+')
    def INT_LIT(self, t):
        t.value = int(t.value)
        return t

    @_(r'"([^\\"]|\\.)*"')
    def STRING_LIT(self, t):
        return t

    @_(r'[A-Za-z_][A-Za-z0-9_]*')
    def IDENT(self, t):
        return t

    @_(r'==')
    def EQ(self, t):
        return t

    @_(r'!=')
    def NE(self, t):
        return t

    @_(r'<=')
    def LE(self, t):
        return t

    @_(r'>=')
    def GE(self, t):
        return t

    @_(r'<')
    def LT(self, t):
        return t

    @_(r'>')
    def GT(self, t):
        return t

    @_(r'\&\&')
    def AND(self, t):
        return t

    @_(r'\|\|')
    def OR(self, t):
        return t

    @_(r'!')
    def NOT(self, t):
        return t

    @_(r'\+')
    def PLUS(self, t):
        return t

    @_(r'-')
    def MINUS(self, t):
        return t

    @_(r'\*')
    def TIMES(self, t):
        return t

    @_(r'/')
    def DIVIDE(self, t):
        return t

    @_(r'%')
    def MOD(self, t):
        return t

    @_(r'=')
    def ASSIGN(self, t):
        return t

    @_(r'\(')
    def LPAREN(self, t):
        return t

    @_(r'\)')
    def RPAREN(self, t):
        return t

    @_(r'\[')
    def LBRACK(self, t):
        return t

    @_(r'\]')
    def RBRACK(self, t):
        return t

    @_(r'\{')
    def LBRACE(self, t):
        return t

    @_(r'\}')
    def RBRACE(self, t):
        return t

    @_(r'\.')
    def DOT(self, t):
        return t

    @_(r',')
    def COMMA(self, t):
        return t

    @_(r';')
    def SEMICOLON(self, t):
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count("\n")
        return t


if __name__ == '__main__':
    lexer = Lexer()
    while True:
        try:
            text = input('> ')
            tokens = lexer.tokenize(text)
            for tok in tokens:
                print(tok)
        except EOFError:
            break
