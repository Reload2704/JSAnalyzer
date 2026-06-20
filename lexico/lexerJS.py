
from ply import lex

tokens = (
    # ===== INICIO APORTE JORGE BRAVO =====
    'COMMENT_LINE',     # // comentario de una línea
    'COMMENT_BLOCK',    # /* comentario de bloque */

    # Aritméticos
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'INCREMENT', 'DECREMENT',

    # Asignación (simple, aditiva, sustractiva)
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN',
    
    # Lógicos / Comparación
    'AND', 'OR', 'NOT',
    'STRICT_EQ', 'EQ', 'NEQ', 'LT', 'GT',
    # ===== FIN APORTE JORGE BRAVO =====

    # ===== INICIO APORTES CECILIA =====
    'NUMBER',          # números enteros o decimales
    'IDENTIFIER',      # identificadores (variables, funciones, etc.)
    # ===== FIN APORTES CECILIA =====

    # ===== INICIO APORTES FIORELLA =====

    # ===== FIN APORTES FIORELLA =====
)

# Lista para registrar los errores léxicos encontrados (usada por el log)
errores_lexicos = []


# =====================================================================
# INICIO APORTE JORGE BRAVO - Comentarios

def t_COMMENT_BLOCK(t):               # comentario de bloque /* ... */
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

t_COMMENT_LINE = r'//[^\n]*'          # comentario de línea // ...

# FIN APORTE JORGE BRAVO - Comentarios
# =====================================================================


# =====================================================================
# INICIO APORTE JORGE BRAVO - Operadores

t_STRICT_EQ    = r'==='     # idéntico

t_EQ           = r'=='      # igual
t_NEQ          = r'!='      # diferente
t_INCREMENT    = r'\+\+'    # incremento
t_DECREMENT    = r'--'      # decremento
t_PLUS_ASSIGN  = r'\+='     # asignación aditiva
t_MINUS_ASSIGN = r'-='      # asignación sustractiva
t_AND          = r'&&'      # AND lógico
t_OR           = r'\|\|'    # OR lógico

t_PLUS         = r'\+'      # suma
t_MINUS        = r'-'       # resta
t_TIMES        = r'\*'      # multiplicación
t_DIVIDE       = r'/'       # división
t_MODULO       = r'%'       # módulo
t_ASSIGN       = r'='       # asignación simple
t_NOT          = r'!'       # NOT lógico
t_LT           = r'<'       # menor
t_GT           = r'>'       # mayor

# FIN APORTE JORGE BRAVO - Operadores
# =====================================================================


# ---------------------------------------------------------------------
# Operandos mínimos (aporte de Cecilia). Incluidos solo para que la
# prueba de operadores/comentarios tenga operandos. Se reemplazan por
# las versiones definitivas al integrar el proyecto.
# ---------------------------------------------------------------------
def t_NUMBER(t):
    r'\d+\.\d+|\d+'
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_$][a-zA-Z0-9_$]*'
    return t


# ---------------------------------------------------------------------
# Manejo de líneas, espacios y errores
# ---------------------------------------------------------------------
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    errores_lexicos.append({
        'caracter': t.value[0],
        'linea': t.lexer.lineno,
        'posicion': t.lexpos,
    })
    print(f"[ERROR LÉXICO] Carácter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)


# Construcción del analizador
lexer = lex.lex()
