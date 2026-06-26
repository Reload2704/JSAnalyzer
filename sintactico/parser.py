# Analizador Lexico - JavaScript (PLY)
# Proyecto LP - ESPOL 2026 PAO II

from ply import lex
from ply import yacc
from lexico.lexerJS import tokens

# ~~~ DECLARACION DE VARIABLES ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO 

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

# FIN APORTE FIORELLA QUIJANO 
# =====================================================================

# ~~~ ESTRUCTURAS DE CONTROL ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO 

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

# FIN APORTE JORGE BRAVO 
# =====================================================================

# ~~~ ESTRUCTURAS DE DATOS ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO 

# FIN APORTE FIORELLA QUIJANO 
# =====================================================================

# =====================================================================
# INICIO APORTE CECILIA MONTES 

# FIN APORTE CECILIA MONTES 
# =====================================================================

# =====================================================================
# INICIO APORTE JORGE BRAVO 

# FIN APORTE JORGE BRAVO 
# =====================================================================

# ~~~ DECLARACIONES DE FUNCIONES ~~~

# =====================================================================
# INICIO APORTE FIORELLA QUIJANO 

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

# FIN APORTE JORGE BRAVO 
# =====================================================================

# ~~~ IMPRESION Y SOLICITUD DE DATOS ~~~

# =====================================================================
# INICIO APORTE JORGE BRAVO 

# FIN APORTE JORGE BRAVO 
# =====================================================================