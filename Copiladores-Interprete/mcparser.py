#mcparser.py
from rich.console import Console
from rich.tree import Tree
import sly
from mclex import Lexer
from mcast import *

console = Console()

class Parser(sly.Parser):
    tokens = Lexer.tokens
    precedence = (
        ('nonassoc', 'IFX'),  # Manejo de else colgante
        ('right', 'ELSE'),     # Precedencia para ELSE
        ('left', 'IF'),
        ('right', '='),       # Precedencia de asignación
        ('left', 'OR', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', '<', 'LE', '>', 'GE'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UNARY', '!'),
    )

    # El nodo raíz del programa
    @_('decl_list')
    def program(self, p):
        root = Program(p.decl_list)
        ast_tree = self.build_ast_tree(root)
        console.print(ast_tree)
        return root

    # Manejo de las declaraciones
    @_('decl_list decl')
    def decl_list(self, p):
        return p.decl_list + [p.decl]

    @_('decl')
    def decl_list(self, p):
        return [p.decl]

    @_('var_decl', 'func_decl', 'continue_stmt')
    def decl(self, p):
        return p[0]

    # Declaración de variables
    @_('type_spec IDENT ";"')
    def var_decl(self, p):
        return VarDeclStmt(p.type_spec, p.IDENT)

    @_('type_spec IDENT "[" "]" ";"')
    def var_decl(self, p):
        return ArrayDeclStmt(p.type_spec, p.IDENT)

    # Especificadores de tipo
    @_('VOID', 'BOOL', 'INT', 'FLOAT')
    def type_spec(self, p):
        return p[0]

    # Declaración de funciones
    @_('type_spec IDENT "(" params ")" compound_stmt')
    def func_decl(self, p):
        return FuncDeclStmt(p.type_spec, p.IDENT, p.params, p.compound_stmt)

    # Parámetros de funciones
    @_('param_list')
    def params(self, p):
        return p[0]

    @_('VOID')
    def params(self, p):
        return []

    @_('param_list "," param')
    def param_list(self, p):
        return p.param_list + [p.param]

    @_('param')
    def param_list(self, p):
        return [p.param]

    @_('type_spec IDENT')
    def param(self, p):
        return VarDeclStmt(p.type_spec, p.IDENT)

    @_('type_spec IDENT "[" "]"')
    def param(self, p):
        return ArrayDeclStmt(p.type_spec, p.IDENT)

    # Cuerpo compuesto de la función
    @_('"{" local_decls stmt_list "}"')
    def compound_stmt(self, p):
        return p.local_decls + p.stmt_list

    @_('decl_list')
    def local_decls(self, p):
        return p.decl_list

    @_('empty')
    def local_decls(self, p):
        return []

    # Sentencias
    @_('stmt_list stmt')
    def stmt_list(self, p):
        return p.stmt_list + [p.stmt]

    @_('stmt')
    def stmt_list(self, p):
        return [p.stmt]

    @_('expr_stmt', 'compound_stmt', 'if_stmt', 'while_stmt', 'return_stmt', 'break_stmt', 'continue_stmt')
    def stmt(self, p):
        return p[0]

    # Expresión de sentencia
    @_('expr ";"')
    def expr_stmt(self, p):
        return p.expr

    @_('";"')
    def expr_stmt(self, p):
        return NullStmt()

    # Sentencia while
    @_('WHILE "(" expr ")" stmt')
    def while_stmt(self, p):
        return WhileStmt(p.expr, p.stmt)

    # Sentencia if (manejo de 'else colgante')
    @_('IF "(" expr ")" stmt ELSE stmt')
    def if_stmt(self, p):
        return IfStmt(p.expr, p.stmt0, p.stmt1)

    # Sentencia if sin else (manejo de 'else colgante')
    @_('IF "(" expr ")" stmt %prec IFX')
    def if_stmt(self, p):
        return IfStmt(p.expr, p.stmt)

    # Sentencias de retorno, break, continue
    @_('RETURN ";"')
    def return_stmt(self, p):
        return ReturnStmt()

    @_('RETURN expr ";"')
    def return_stmt(self, p):
        return ReturnStmt(p.expr)

    @_('BREAK ";"')
    def break_stmt(self, p):
        return BreakStmt()

    @_('CONTINUE ";"')
    def continue_stmt(self, p):
        return ContinueStmt()

    # Expresiones
    @_('IDENT "=" expr')
    def expr(self, p):
        return VarAssignmentExpr(p.IDENT, p.expr)

    @_('IDENT "[" expr "]" "=" expr')
    def expr(self, p):
        return ArrayAssignmentExpr(p.IDENT, p.expr0, p.expr1)

    @_('expr OR expr', 'expr AND expr', 'expr EQ expr', 'expr NE expr',
       'expr LE expr', 'expr "<" expr', 'expr GE expr', 'expr ">" expr',
       'expr "+" expr', 'expr "-" expr', 'expr "*" expr', 'expr "/" expr',
       'expr "%" expr')
    def expr(self, p):
        return BinaryOpExpr(p[1], p.expr0, p.expr1)

    @_('"!" expr', '"-" expr %prec UNARY', '"+" expr %prec UNARY')
    def expr(self, p):
        return UnaryOpExpr(p[0], p.expr)

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('IDENT')
    def expr(self, p):
        return VarExpr(p.IDENT)

    @_('IDENT "[" expr "]"')
    def expr(self, p):
        return ArrayLookupExpr(p.IDENT, p.expr)

    @_('IDENT "(" args ")"')
    def expr(self, p):
        return CallExpr(p.IDENT, p.args)

    @_('IDENT "." SIZE')
    def expr(self, p):
        return ArraySizeExpr(p.IDENT)

    @_('BOOL_LIT', 'INT_LIT', 'FLOAT_LIT', 'STRING_LIT')
    def expr(self, p):
        return ConstExpr(p[0])

    @_('NEW type_spec "[" expr "]"')
    def expr(self, p):
        return NewArrayExpr(p.type_spec, p.expr)

    # Argumentos de las funciones
    @_('arg_list')
    def args(self, p):
        return p.arg_list

    @_('arg_list "," expr')
    def arg_list(self, p):
        return p.arg_list + [p.expr]

    @_('expr')
    def arg_list(self, p):
        return [p.expr]

    @_('')  # Define explícitamente la regla de `empty`
    def empty(self, p):
        return NullStmt()

    # Manejo de errores
    def error(self, p):
        if p:
            lineno = p.lineno
            value = p.value
            console.print(f'[bold red]Error de sintaxis[/bold red] en línea {lineno}: {value}')
            print(f"Error en el token: {value}")  # Agregado para depuración
        else:
            console.print(f'[bold red]Error de sintaxis[/bold red] en línea EOF: Se esperaba más información.')

    # Método para construir el árbol del AST con Rich
    def build_ast_tree(self, node):
        tree = Tree(f"{node.__class__.__name__}")
        for field, value in node.__dict__.items():
            if isinstance(value, list):
                if not value:
                    continue
                branch = Tree(f"{field} (List)")
                for item in value:
                    if isinstance(item, Node):
                        branch.add(self.build_ast_tree(item))
                    else:
                        branch.add(str(item))
                tree.add(branch)
            elif isinstance(value, Node):
                tree.add(self.build_ast_tree(value))
            else:
                tree.add(f"{field}: {value}")
        return tree

    # Para mostrar el conflicto
    def shift_reduce_conflict(self, token):
        console.print(f'[bold yellow]Shift/Reduce Conflict[/bold yellow]: Token "{token}" podría causar un conflicto.')

if __name__ == '__main__':
    parser = Parser()
    lexer = Lexer()
    while True:
        try:
            text = input('> ')
            tokens = lexer.tokenize(text)
            for tok in tokens:
                print(tok)
            parser.parse(lexer.tokenize(text))
        except EOFError:
            break
