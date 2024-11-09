#mcontext.py
'''
Clase de nivel superior que contiene todo sobre el 
análisis/ejecución de un programa en Mini-C++

Sirve como repositorio de información sobre el programa,
incluido el código fuente, informe de errores, etc.
'''
'''
Clase de nivel superior que contiene todo sobre el 
análisis/ejecución de un programa en Mini-C++

Sirve como repositorio de información sobre el programa,
incluido el código fuente, informe de errores, etc.
'''
from rich import print
from mcast import Node
from mclex import Lexer
from mcparser import Parser

class Context:
    def __init__(self):
        self.lexer = Lexer()  # Crear instancia del Lexer
        self.ast = None
        self.have_errors = False
        self.source = ""  # Inicializamos source para almacenar el código fuente
        self.parser = Parser()  # Aseguramos la instancia del parser

    def parse(self, source):
        self.source = source  # Almacenar el código fuente
        # Tokenizar directamente el código fuente
        tokens = self.lexer.tokenize(source)  # Cambiado a tokenize
        self.ast = []  # Inicializar el AST como una lista vacía

        # Mostrar los tokens generados (para depuración)
        for tok in tokens:
            print(tok)

        # Llamar al parser para procesar los tokens
        self.parser.parse(tokens)  # Asegúrate de que tu parser esté listo para recibir tokens

    def run(self):
        if not self.have_errors:
            # Aquí puedes agregar la lógica de ejecución del AST si es necesario
            print("[green]Ejecución completada sin errores[/green]")

    def find_source(self, node):
        indices = self.parser.index_position(node)
        if indices:
            return self.source[indices[0]:indices[1]]
        else:
            return f"{type(node).__name__} (fuente no disponible)"

    def error(self, position, message):
        if isinstance(position, Node):
            lineno = self.parser.line_position(position)
            (start, end) = self.parser.index_position(position)

            # Encontrar la línea correspondiente al error
            while start >= 0 and self.source[start] != '\n':
                start -= 1
            start += 1
            while end < len(self.source) and self.source[end] != '\n':
                end += 1

            # Mostrar el error en contexto
            print()
            print(self.source[start:end])
            print(" " * (start), end='')  # Se cambió part_start por start
            print("^" * (end - start))  # Se cambió part_end y part_start
            print(f"{lineno}: {message}")
        else:
            print(f"{position}: {message}")
        self.have_errors = True
