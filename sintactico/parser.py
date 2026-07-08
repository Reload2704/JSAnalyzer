# Analizador Sintactico - JavaScript (PLY)
# Proyecto LP - ESPOL 2026 PAO II
#
# Construye el AST (Arbol de Sintaxis Abstracta) a partir de los tokens del
# analizador lexico. El AST se entrega al analizador semantico.
#
# CONVENCION DE NODOS (tuplas: etiqueta primero, linea al final):
#   ('num', valor, linea) | ('str', valor, linea) | ('bool', valor, linea)
#   ('id', nombre, linea)
#   ('llamada', nombre, [args], linea)          -> Number("25"), miFuncion(a,b)
#   ('impresion', objeto, metodo, [args], linea)-> console.log(...)
#   ('decl', tipo, nombre, valor, linea)        -> tipo: 'let'|'const'|'var'
#   ('binaria', op, izq, der, linea) | ('unario', op, expr, linea)
#   ('while', cond, cuerpo, linea)
#   ('for', init, cond, incr, cuerpo, linea)
#   ('if', cond, cuerpo, sino, linea)
#   ('break', linea)
#   ('funcion', nombre, [params], cuerpo, retorno, linea)
#   ('return', expr, linea)
#   ('array', [elems], linea) | ('acceso', nombre, indice, linea)
#   ('objeto', [(clave, valor), ...], linea)
# Un programa es una lista de sentencias.

from ply import yacc

# Importacion robusta del lexer (desde la raiz o agregando 'lexico' al path)
try:
    from lexico.lexerJS import tokens
    import lexico.lexerJS as lexmod
except ImportError:
    from lexerJS import tokens
    import lexerJS as lexmod

# Lista de errores sintacticos (mensajes personalizados)
errores_sintacticos = []

# Simbolo inicial de la gramatica
start = 'programa'

# Precedencia y asociatividad de operadores (de menor a mayor prioridad)
# (unifica la precedencia aritmetica definida por Cecilia Montes)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ', 'STRICT_EQ', 'STRICT_NEQ'),
    ('left', 'LT', 'GT', 'LTE', 'GTE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
)


# =====================================================================
# ESTRUCTURA DEL PROGRAMA (infraestructura comun / Jorge Bravo)
# =====================================================================
def p_programa(p):
    '''
    programa : lista_sentencias
    '''
    p[0] = p[1]


def p_lista_sentencias(p):
    '''
    lista_sentencias : sentencia lista_sentencias
                     | empty
    '''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []


def p_sentencia(p):
    '''
    sentencia : declaracion
              | estructura_control
              | impresion
              | expresion SEMICOLON
              | BREAK SEMICOLON
    '''
    if len(p) == 3 and p.slice[1].type == 'BREAK':
        p[0] = ('break', p.lineno(1))
    else:
        p[0] = p[1]


# ~~~ DECLARACION DE VARIABLES ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO
def p_declaracion_let(p):
    '''
    declaracion : LET IDENTIFIER ASSIGN expresion SEMICOLON
    '''
    p[0] = ('decl', 'let', p[2], p[4], p.lineno(1))
# FIN APORTE FIORELLA QUIJANO
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES
def p_declaracion_const(p):
    '''
    declaracion : CONST IDENTIFIER ASSIGN expresion SEMICOLON
    '''
    p[0] = ('decl', 'const', p[2], p[4], p.lineno(1))
# FIN APORTE CECILIA MONTES
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
def p_declaracion_var(p):
    '''
    declaracion : VAR IDENTIFIER ASSIGN expresion SEMICOLON
                | VAR IDENTIFIER SEMICOLON
    '''
    if len(p) == 6:
        p[0] = ('decl', 'var', p[2], p[4], p.lineno(1))
    else:
        p[0] = ('decl', 'var', p[2], None, p.lineno(1))
# FIN APORTE JORGE BRAVO
# =====================================================================

# ~~~ EXPRESIONES ARITMETICAS ~~~

# =====================================================================
# INICIO APORTE CECILIA MONTES
def p_expresion_binaria(p):
    '''
    expresion : expresion PLUS expresion
              | expresion MINUS expresion
              | expresion TIMES expresion
              | expresion DIVIDE expresion
              | expresion MODULO expresion
    '''
    p[0] = ('binaria', p[2], p[1], p[3], p.lineno(2))


def p_expresion_valor(p):
    '''
    expresion : NUMBER
              | BIGINT
              | STRING
              | BOOLEAN
              | IDENTIFIER
    '''
    tipo = p.slice[1].type
    if tipo in ('NUMBER', 'BIGINT'):
        p[0] = ('num', p[1], p.lineno(1))
    elif tipo == 'STRING':
        p[0] = ('str', p[1], p.lineno(1))
    elif tipo == 'BOOLEAN':
        p[0] = ('bool', p[1], p.lineno(1))
    else:
        p[0] = ('id', p[1], p.lineno(1))


def p_expresion_parentesis(p):
    '''
    expresion : LPAREN expresion RPAREN
    '''
    p[0] = p[2]
# FIN APORTE CECILIA MONTES
# =====================================================================

# ~~~ EXPRESIONES BOOLEANAS ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO
def p_expresion_booleana(p):
    '''
    expresion : expresion AND expresion
              | expresion OR expresion
              | expresion EQ expresion
              | expresion STRICT_EQ expresion
              | expresion NEQ expresion
              | expresion STRICT_NEQ expresion
              | expresion LT expresion
              | expresion GT expresion
              | expresion LTE expresion
              | expresion GTE expresion
    '''
    p[0] = ('binaria', p[2], p[1], p[3], p.lineno(2))


def p_expresion_not(p):
    '''
    expresion : NOT expresion
    '''
    p[0] = ('unario', '!', p[2], p.lineno(1))
# FIN APORTE FIORELLA QUIJANO
# =====================================================================

# ~~~ ESTRUCTURAS DE CONTROL ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO
def p_while(p):
    '''
    estructura_control : WHILE LPAREN expresion RPAREN bloque
    '''
    p[0] = ('while', p[3], p[5], p.lineno(1))
# FIN APORTE FIORELLA QUIJANO
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES
def p_for(p):
    '''
    estructura_control : FOR LPAREN declaracion condicion SEMICOLON incremento RPAREN bloque
    '''
    p[0] = ('for', p[3], p[4], p[6], p[8], p.lineno(1))


def p_incremento(p):
    '''
    incremento : IDENTIFIER INCREMENT
               | IDENTIFIER DECREMENT
    '''
    p[0] = ('incremento', p[1], p[2], p.lineno(1))


def p_condicion(p):
    '''
    condicion : expresion LT expresion
              | expresion GT expresion
              | expresion EQ expresion
              | expresion STRICT_EQ expresion
              | expresion NEQ expresion
    '''
    p[0] = ('binaria', p[2], p[1], p[3], p.lineno(2))
# FIN APORTE CECILIA MONTES
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
def p_if_else(p):
    '''
    estructura_control : IF LPAREN expresion RPAREN bloque
                       | IF LPAREN expresion RPAREN bloque ELSE bloque
    '''
    sino = p[7] if len(p) == 8 else None
    p[0] = ('if', p[3], p[5], sino, p.lineno(1))
# FIN APORTE JORGE BRAVO
# =====================================================================

# ~~~ ESTRUCTURAS DE DATOS ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO
def p_objeto_simple(p):
    '''
    expresion : LKEY pares_clave_valor RKEY
              | LKEY empty RKEY
    '''
    p[0] = ('objeto', p[2] if p[2] else [], p.lineno(1))


def p_pares_clave_valor(p):
    '''
    pares_clave_valor : IDENTIFIER COLON expresion
                      | IDENTIFIER COLON expresion COMMA pares_clave_valor
    '''
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = [(p[1], p[3])] + p[5]
# FIN APORTE FIORELLA QUIJANO
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES
# Objeto anidado: el valor de una propiedad ya puede ser otro objeto,
# porque en 'pares_clave_valor' el valor es una 'expresion' y un objeto
# ('objeto_simple') es una expresion. No se requiere una regla extra.
# (Regla 'valor : expresion | objeto' pendiente; queda cubierta por lo anterior.)
# FIN APORTE CECILIA MONTES
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
def p_array(p):
    '''
    expresion : LBRACKET elementos RBRACKET
    '''
    p[0] = ('array', p[2], p.lineno(1))


def p_elementos(p):
    '''
    elementos : expresion
              | elementos COMMA expresion
              | empty
    '''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_array_acceso(p):
    '''
    expresion : IDENTIFIER LBRACKET expresion RBRACKET
    '''
    p[0] = ('acceso', p[1], p[3], p.lineno(1))
# FIN APORTE JORGE BRAVO
# =====================================================================

# ~~~ DECLARACIONES DE FUNCIONES ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO
def p_funcion_tradicional(p):
    '''
    declaracion : FUNCTION IDENTIFIER LPAREN parametros RPAREN LKEY lista_sentencias RETURN expresion SEMICOLON RKEY
    '''
    retorno = ('return', p[9], p.lineno(8))
    cuerpo = p[7] + [retorno]
    p[0] = ('funcion', p[2], p[4], cuerpo, retorno, p.lineno(1))
# FIN APORTE FIORELLA QUIJANO
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES
def p_arrow_function(p):
    '''
    declaracion : CONST IDENTIFIER ASSIGN LPAREN parametros RPAREN ARROW bloque
    '''
    p[0] = ('funcion', p[2], p[5], p[8], None, p.lineno(1))


def p_parametros(p):
    '''
    parametros : IDENTIFIER
               | parametros COMMA IDENTIFIER
               | empty
    '''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_bloque(p):
    '''
    bloque : LKEY lista_sentencias RKEY
    '''
    p[0] = p[2]


def p_empty(p):
    '''
    empty :
    '''
    p[0] = None
# FIN APORTE CECILIA MONTES
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
def p_funcion_expresion(p):
    '''
    expresion : FUNCTION LPAREN parametros RPAREN bloque
    '''
    p[0] = ('funcion', None, p[3], p[5], None, p.lineno(1))
# FIN APORTE JORGE BRAVO
# =====================================================================

# ~~~ IMPRESION Y SOLICITUD DE DATOS ~~~

# =====================================================================
# INICIO APORTE JORGE BRAVO
def p_impresion(p):
    '''
    impresion : IDENTIFIER DOT IDENTIFIER LPAREN argumentos RPAREN SEMICOLON
    '''
    p[0] = ('impresion', p[1], p[3], p[5], p.lineno(1))


def p_solicitud(p):
    '''
    expresion : IDENTIFIER LPAREN argumentos RPAREN
    '''
    p[0] = ('llamada', p[1], p[3], p.lineno(1))


def p_argumentos(p):
    '''
    argumentos : expresion
               | argumentos COMMA expresion
               | empty
    '''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = p[1] + [p[3]]
# FIN APORTE JORGE BRAVO
# =====================================================================


# =====================================================================
# MANEJO DE ERRORES SINTACTICOS (mensaje personalizado)
# =====================================================================
def p_error(p):
    if p:
        errores_sintacticos.append(
            "Error Sintactico [Linea {}]: token inesperado '{}' ({}).".format(
                p.lineno, p.value, p.type
            )
        )
    else:
        errores_sintacticos.append(
            "Error Sintactico: fin de archivo inesperado (revise llaves o ';')."
        )


# =====================================================================
# Filtro de comentarios: el analisis lexico reconoce los comentarios como
# tokens (y los reporta), pero NO son parte de la gramatica. Este envoltorio
# los descarta antes de que lleguen al parser.
# =====================================================================
class _LexerSinComentarios:
    _IGNORAR = ('COMMENT_LINE', 'COMMENT_BLOCK')

    def __init__(self, lexer):
        self._lexer = lexer

    def input(self, data):
        self._lexer.input(data)

    def token(self):
        tok = self._lexer.token()
        while tok is not None and tok.type in self._IGNORAR:
            tok = self._lexer.token()
        return tok


# Se construye el parser una sola vez al importar el modulo.
parser = yacc.yacc(write_tables=False, debug=False)


def parsear(codigo):
    """Analiza el codigo fuente y devuelve (ast, errores_sintacticos)."""
    errores_sintacticos.clear()
    lexmod.lexer.lineno = 1
    ast = parser.parse(codigo, lexer=_LexerSinComentarios(lexmod.lexer))
    return ast, errores_sintacticos
