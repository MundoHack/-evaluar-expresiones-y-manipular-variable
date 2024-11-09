#mccinterp.py
from mclex import Lexer  # Cambia MCLexer por Lexer
from mcparser import Parser
from mcast import (ASTNode, PrintfNode, SprintfNode, 
                    PostIncrementNode, PreIncrementNode, 
                    PlusAssignNode, MinusAssignNode, 
                    MultAssignNode, DivAssignNode, 
                    LogicalAndNode, LogicalOrNode, NullNode)

# Definir la clase InterpreteExtendido directamente, sin necesidad de importarla
class InterpreteExtendido:
    
    def __init__(self):
        # Inicializa un diccionario para las variables
        self.env = {}

    def visit(self, node):
        """Método principal de recorrido del AST que delega a los métodos específicos de cada nodo."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    
    def generic_visit(self, node):
        """Método genérico para nodos no manejados explícitamente."""
        raise Exception(f"No visit method for {type(node).__name__}")

    def visit_PrintfNode(self, node):
        # Simulación básica de `printf`, reemplazando códigos de escape
        formatted_string = node.string.replace('\\n', '\n').replace('\\t', '\t')
        print(formatted_string % self.visit(node.expr))

    def visit_SprintfNode(self, node):
        # `sprintf` simula la construcción de una cadena sin imprimir
        formatted_string = node.string.replace('\\n', '\n').replace('\\t', '\t')
        return formatted_string % self.visit(node.expr)

    def visit_PostIncrementNode(self, node):
        # Guarda el valor actual, incrementa después
        value = self.visit(node.expr)
        self.env[node.expr.name] = value + 1
        return value

    def visit_PreIncrementNode(self, node):
        # Incrementa antes y devuelve el nuevo valor
        value = self.visit(node.expr) + 1
        self.env[node.expr.name] = value
        return value

    def visit_PostDecrementNode(self, node):
        # Guarda el valor actual, decrementa después
        value = self.visit(node.expr)
        self.env[node.expr.name] = value - 1
        return value

    def visit_PreDecrementNode(self, node):
        # Decrementa antes y devuelve el nuevo valor
        value = self.visit(node.expr) - 1
        self.env[node.expr.name] = value
        return value

    def visit_PlusAssignNode(self, node):
        # `x += value`
        current_value = self.env[node.identifier.name]
        self.env[node.identifier.name] = current_value + self.visit(node.expr)
        return self.env[node.identifier.name]

    def visit_MinusAssignNode(self, node):
        # `x -= value`
        current_value = self.env[node.identifier.name]
        self.env[node.identifier.name] = current_value - self.visit(node.expr)
        return self.env[node.identifier.name]

    def visit_MultAssignNode(self, node):
        # `x *= value`
        current_value = self.env[node.identifier.name]
        self.env[node.identifier.name] = current_value * self.visit(node.expr)
        return self.env[node.identifier.name]

    def visit_DivAssignNode(self, node):
        # `x /= value`
        current_value = self.env[node.identifier.name]
        if self.visit(node.expr) == 0:
            raise ZeroDivisionError("Division by zero in '/=' operator.")
        self.env[node.identifier.name] = current_value / self.visit(node.expr)
        return self.env[node.identifier.name]

    def visit_LogicalAndNode(self, node):
        # Evaluación de circuito-corto para `&&`
        left = self.visit(node.left)
        if not left:
            return False
        return self.visit(node.right)

    def visit_LogicalOrNode(self, node):
        # Evaluación de circuito-corto para `||`
        left = self.visit(node.left)
        if left:
            return True
        return self.visit(node.right)

    def visit_NullNode(self, node):
        # Maneja `NULL` como un valor especial
        return None

    def visit_Identifier(self, node):
        # Permite el uso de NULL en expresiones
        value = self.env.get(node.name)
        if value is None:
            raise NameError(f"Variable '{node.name}' is not defined.")
        return value

    # Otras visitas a nodos aquí...

# Ejecución principal de ejemplo:
if __name__ == '__main__':
    lexer = Lexer()  # Instancia de Lexer en lugar de MCLexer
    parser = Parser()
    code = """
    // Prueba de printf con códigos de escape
printf("Hola\\nMundo\\tCon\\tTabulacion");
    
    // Prueba de operadores ++ y -- en sus formas prefijas y postfijas
int a = 5;
int b = a++;    // b = 5, a = 6 (postfijo)
int c = ++a;    // c = 7, a = 7 (prefijo)
int d = a--;    // d = 7, a = 6 (postfijo)
int e = --a;    // e = 5, a = 5 (prefijo)
printf("Valores: b=%d, c=%d, d=%d, e=%d\\n", b, c, d, e);

    // Prueba de operadores de asignación compuesta
int x = 10;
x += 5;    // x = 15
x -= 3;    // x = 12
x *= 2;    // x = 24
x /= 4;    // x = 6
printf("Resultado de x: %d\\n", x);

    // Prueba de evaluación de circuito-corto
int y = 0;
int z = 10;
int res1 = (y != 0) && (z /= y);  // res1 = 0 (corto-circuito)
int res2 = (y == 0) || (z /= 2);  // res2 = 1, z = 5 (corto-circuito)
printf("Resultado de z: %d, res1: %d, res2: %d\\n", z, res1, res2);

    // Prueba de valor NULL
int* p = NULL;
if (p == NULL) {
    printf("Puntero es NULL\\n");
}
    """
    
    # Tokeniza el código y muestra los tokens generados para depuración
    tokens = lexer.tokenize(code)
    for token in tokens:
        print(token)

    ast = parser.parse(tokens)
    interpreter = InterpreteExtendido()
 
    if ast is not None:
        interpreter.visit(ast)
    else:
        print("El AST es None. El parseo falló.")
