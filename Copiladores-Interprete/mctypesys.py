# mctypesys.py
'''
Sistema de Tipos
================
Este archivo implementa las caracteristicas básicas del sistema de tipos.
Hay mucha flexibilidad posible aquí, pero la mejor estrategia podría ser
no pensar demasiado en el problema. Al menos no al principio.
Estos son los requisitos básicos mínimos:

1. Los tipos tienen identidad (por ejemplo, como mínimo un nombre como
   'int', 'float', 'bool')
2. Los tipos deben ser comparables. (por ejemplo, 'int' != 'float')
3. Los tipos admiten diferentes operadores (por ejemplo: +, -, *, /, etc.)

Una forma de lograr todos estos objetivos es comenzar con algun tipo de 
enfoque basado en tablas. No es lo mas sofisticado, pero funciona como
punto de partida.

Puede volver y refactorizar el sistema de tipos mas tarde.
'''
# Conjunto válido de tipos
typenames = {'int', 'float', 'bool'}

# Tabla de operaciones binarias y su tipo resultante
_binary_ops = {
    # Operaciones int
    ('+', 'int', 'int'): 'int',
    ('-', 'int', 'int'): 'int',
    ('*', 'int', 'int'): 'int',
    ('/', 'int', 'int'): 'int',

    ('<', 'int', 'int'): 'bool',
    ('<=', 'int', 'int'): 'bool',
    ('>', 'int', 'int'): 'bool',
    ('>=', 'int', 'int'): 'bool',
    ('==', 'int', 'int'): 'bool',
    ('!=', 'int', 'int'): 'bool',

    # Operaciones float
    ('+', 'float', 'float'): 'float',
    ('-', 'float', 'float'): 'float',
    ('*', 'float', 'float'): 'float',
    ('/', 'float', 'float'): 'float',

    ('<', 'float', 'float'): 'bool',
    ('<=', 'float', 'float'): 'bool',
    ('>', 'float', 'float'): 'bool',
    ('>=', 'float', 'float'): 'bool',
    ('==', 'float', 'float'): 'bool',
    ('!=', 'float', 'float'): 'bool',

    # Operaciones booleanas
    ('&&', 'bool', 'bool'): 'bool',
    ('||', 'bool', 'bool'): 'bool',
    ('==', 'bool', 'bool'): 'bool',
    ('!=', 'bool', 'bool'): 'bool',
}

# Tabla de operaciones unarias y su tipo resultante
_unary_ops = {
    ('+', 'int'): 'int',
    ('-', 'int'): 'int',
    ('+', 'float'): 'float',
    ('-', 'float'): 'float',
    ('!', 'bool'): 'bool',
}

def lookup_type(name):
    '''Devuelve el tipo correspondiente a un nombre.'''
    return name if name in typenames else None

def check_binary_op(op, left, right):
    '''Verifica si una operación binaria es válida.'''
    return _binary_ops.get((op, left, right))

def check_unary_op(op, expr):
    '''Verifica si una operación unaria es válida.'''
    return _unary_ops.get((op, expr))