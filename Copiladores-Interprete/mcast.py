#mcast.py
from dataclasses import dataclass, field
from graphviz import Digraph
from multimethod import multimeta
from typing import Union, List, Optional

# Clases Abstractas

@dataclass
class Visitor(metaclass=multimeta):
    """Clase abstracta del Patrón Visitor."""
    pass

@dataclass
class Node:
    def accept(self, v: Visitor, *args, **kwargs):
        return v.visit(self, *args, **kwargs)

@dataclass
class Statement(Node):
    pass

@dataclass
class Expression(Node):
    pass

# Nodos AST específicos

@dataclass
class ASTNode(Node):
    """Clase base para los nodos del AST."""
    pass

@dataclass
class PrintfNode(ASTNode):
    string: str
    expr: Expression

@dataclass
class SprintfNode(ASTNode):
    string: str
    expr: Expression

@dataclass
class PostIncrementNode(ASTNode):
    expr: Expression

@dataclass
class PreIncrementNode(ASTNode):
    expr: Expression

@dataclass
class PlusAssignNode(ASTNode):
    identifier: str
    expr: Expression

@dataclass
class MinusAssignNode(ASTNode):
    identifier: str
    expr: Expression

@dataclass
class MultAssignNode(ASTNode):
    identifier: str
    expr: Expression

@dataclass
class DivAssignNode(ASTNode):
    identifier: str
    expr: Expression

@dataclass
class LogicalAndNode(ASTNode):
    left: Expression
    right: Expression

@dataclass
class LogicalOrNode(ASTNode):
    left: Expression
    right: Expression

@dataclass
class NullNode(ASTNode):
    pass


# Clases Concretas

@dataclass
class Program(Statement):
    stmts: List[Statement] = field(default_factory=list)

@dataclass
class NullStmt(Statement):
    pass

@dataclass
class FuncDeclStmt(Statement):
    type: str
    ident: str
    params: List[Statement] = field(default_factory=list)
    stmts: List[Statement] = field(default_factory=list)

@dataclass
class VarDeclStmt(Statement):
    type: str
    ident: str
    expr: Optional[Expression] = None  # Agregado para compatibilidad.

@dataclass
class ArrayDeclStmt(Statement):
    type: str
    ident: str

@dataclass
class WhileStmt(Statement):
    expr: Expression
    stmt: Statement

@dataclass
class IfStmt(Statement):
    expr: Expression
    then: Statement
    else_: Optional[Statement] = None

@dataclass
class ReturnStmt(Statement):
    expr: Optional[Expression] = None

@dataclass
class BreakStmt(Statement):
    pass

@dataclass
class ContinueStmt(Statement):
    pass

@dataclass
class CompoundStmt(Statement):
    decls: List[VarDeclStmt] = field(default_factory=list)
    stmts: List[Statement] = field(default_factory=list)


@dataclass
class ConstExpr(Expression):
    value: Union[bool, int, float]

@dataclass
class NewArrayExpr(Expression):
    type: str
    expr: Expression

@dataclass
class VarExpr(Expression):
    ident: str

@dataclass
class ArrayLoockupExpr(Expression):
    ident: str
    expr: Expression

@dataclass
class CallExpr(Expression):
    func: Expression  # Cambio: para compatibilidad con Checker.
    args: List[Expression] = field(default_factory=list)

@dataclass
class VarAssignmentExpr(Expression):
    ident: str
    expr: Expression

@dataclass
class ArrayAssignmentExpr(Expression):
    ident: str
    ndx: Expression
    expr: Expression

@dataclass
class BinaryOpExpr(Expression):
    opr: str
    left: Expression
    right: Expression

@dataclass
class UnaryOpExpr(Expression):
    opr: str
    expr: Expression

@dataclass
class ArraySizeExpr(Expression):
    ident: str

# Clase que genera el AST en dot

class DotRender(Visitor):
    default_node = {'shape': 'box', 'color': 'deepskyblue', 'style': 'filled'}
    default_edge = {'arrowhead': 'none'}

    def __init__(self, name='AST'):
        self.dot = Digraph(name)
        self.dot.attr('node', **self.default_node)
        self.dot.attr('edge', **self.default_edge)

    def visit(self, n: Program):
        pass

    def visit(self, n: NullStmt):
        pass

    def visit(self, n: FuncDeclStmt):
        pass

    def visit(self, n: VarDeclStmt):
        pass

class ArrayLookupExpr(Node):
    def __init__(self, array_name, index_expr):
        self.array_name = array_name  # Nombre del arreglo (IDENT)
        self.index_expr = index_expr  # Expresión del índice (expr)

    def __repr__(self):
        return f"ArrayLookupExpr(array_name={self.array_name}, index_expr={self.index_expr})"

    # Método para evaluar el acceso al arreglo (opcional, según tus necesidades)
    def evaluate(self, context):
        array = context.get(self.array_name)
        if array is not None and isinstance(array, list):
            index = self.index_expr.evaluate(context)
            if 0 <= index < len(array):
                return array[index]
            else:
                raise IndexError(f"Índice {index} fuera de los límites para el arreglo '{self.array_name}'")
        else:
            raise ValueError(f"{self.array_name} no es un arreglo o no existe en el contexto")
