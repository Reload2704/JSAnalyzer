# Analizador Lexico - JavaScript (PLY)
# Proyecto LP - ESPOL 2026 PAO II

from ply import lex
from ply import yacc
from lexico.lexerJS import tokens

# ~~~ DECLARACION DE VARIABLES ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO 
def p_declaracion_let(p):
    '''
    declaracion : LET IDENTIFIER ASSIGN expresion SEMICOLON
    '''
    pass
# FIN APORTE FIORELLA QUIJANO
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES 
def p_declaracion_const(p):
    '''
    declaracion : CONST IDENTIFIER ASSIGN expresion SEMICOLON
    '''

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
)
# FIN APORTE CECILIA MONTES
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
# Declaracion de variables con 'var' (con o sin inicializacion)
def p_declaracion_var(p):
    '''
    declaracion : VAR IDENTIFIER ASSIGN expresion SEMICOLON
                | VAR IDENTIFIER SEMICOLON
    '''
    pass
# FIN APORTE JORGE BRAVO
# =====================================================================

# ~~~ EXPRESIONES ARITMETICAS ~~~

# =====================================================================
# INICION APORTE CECILIA MONTES
def p_expresion_binaria(p):
    '''
    expresion : expresion PLUS expresion
              | expresion MINUS expresion
              | expresion TIMES expresion
              | expresion DIVIDE expresion
              | expresion MODULO expresion
    '''

def p_expresion_valor(p):
    '''
    expresion : NUMBER
              | BIGINT
              | STRING
              | BOOLEAN
              | IDENTIFIER
    '''

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
    pass

def p_expresion_not(p):
    '''
    expresion : NOT expresion
    '''
    pass
# FIN APORTE FIORELLA QUIJANO 
# =====================================================================

# ~~~ ESTRUCTURAS DE CONTROL ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO 
def p_while(p):
    '''
    estructura_control : WHILE LPAREN expresion RPAREN bloque
    '''
    pass
# FIN APORTE FIORELLA QUIJANO 
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES 
def p_for(p):
    '''
    estructura_control : FOR LPAREN declaracion condicion SEMICOLON incremento RPAREN bloque
    '''

def p_incremento(p):
    '''
    incremento : IDENTIFIER INCREMENT
               | IDENTIFIER DECREMENT
    '''

def p_condicion(p):
    '''
    condicion : expresion LT expresion
              | expresion GT expresion
              | expresion EQ expresion
              | expresion STRICT_EQ expresion
              | expresion NEQ expresion
    '''

# FIN APORTE CECILIA MONTES 
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
# Estructura de control if / if-else.
# La condicion es una expresion (incluye comparaciones y booleanas).
def p_if_else(p):
    '''
    estructura_control : IF LPAREN expresion RPAREN bloque
                       | IF LPAREN expresion RPAREN bloque ELSE bloque
    '''
    pass
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
    pass

def p_pares_clave_valor(p):
    '''
    pares_clave_valor : IDENTIFIER COLON expresion
                      | IDENTIFIER COLON expresion COMMA pares_clave_valor
    '''
    pass
# FIN APORTE FIORELLA QUIJANO 
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES 

# FIN APORTE CECILIA MONTES 
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
# Estructura de datos: Array (arreglo literal y acceso por indice)
def p_array(p):
    '''
    expresion : LBRACKET elementos RBRACKET
    '''
    pass

def p_elementos(p):
    '''
    elementos : expresion
              | elementos COMMA expresion
              | empty
    '''
    pass

def p_array_acceso(p):
    '''
    expresion : IDENTIFIER LBRACKET expresion RBRACKET
    '''
    pass
# FIN APORTE JORGE BRAVO
# =====================================================================

# ~~~ DECLARACIONES DE FUNCIONES ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO 
def p_funcion_tradicional(p):
    '''
    declaracion : FUNCTION IDENTIFIER LPAREN parametros RPAREN LKEY lista_sentencias RETURN expresion SEMICOLON RKEY
    '''
    pass
# FIN APORTE FIORELLA QUIJANO 
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES 
def p_arrow_function(p):
    '''
    declaracion : CONST IDENTIFIER ASSIGN LPAREN parametros RPAREN ARROW bloque
    '''

def p_parametros(p):
    '''
    parametros : IDENTIFIER
               | parametros COMMA IDENTIFIER
               | empty
    '''

def p_bloque(p):
    '''
    bloque : LKEY lista_sentencias RKEY
    '''

def p_empty(p):
    '''
    empty :
    '''
    pass

# FIN APORTE CECILIA MONTES 
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO
# Funcion como expresion (function expression).
# Al ser una expresion se puede asignar a una variable:
#   var saludar = function(persona) { ... };
def p_funcion_expresion(p):
    '''
    expresion : FUNCTION LPAREN parametros RPAREN bloque
    '''
    pass
# FIN APORTE JORGE BRAVO
# =====================================================================

# ~~~ IMPRESION Y SOLICITUD DE DATOS ~~~

# =====================================================================
# INICIO APORTE JORGE BRAVO
# Impresion: console.log(...) como sentencia.
def p_impresion(p):
    '''
    impresion : IDENTIFIER DOT IDENTIFIER LPAREN argumentos RPAREN SEMICOLON
    '''
    pass

# Solicitud de datos / llamada a funcion como expresion:
#   prompt("..."), alert("..."), miFuncion(a, b)
def p_solicitud(p):
    '''
    expresion : IDENTIFIER LPAREN argumentos RPAREN
    '''
    pass

# Lista de argumentos para impresion y llamadas a funcion
def p_argumentos(p):
    '''
    argumentos : expresion
               | argumentos COMMA expresion
               | empty
    '''
    pass
# FIN APORTE JORGE BRAVO
# =====================================================================