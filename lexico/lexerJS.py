# Analizador Lexico - JavaScript (PLY)
# Proyecto LP - ESPOL 2026 PAO II

from ply import lex

tokens = (
    # ===== INICIO APORTE JORGE BRAVO =====
    'COMMENT_LINE',     # // comentario de una linea
    'COMMENT_BLOCK',    # /* comentario de bloque */

    # Aritmeticos
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'INCREMENT', 'DECREMENT',

    # Asignacion (simple, aditiva, sustractiva)
    'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN',

    # Logicos / Comparacion
    'AND', 'OR', 'NOT',
    'STRICT_EQ', 'EQ', 'NEQ', 'LT', 'GT',
    # ===== FIN APORTE JORGE BRAVO =====

    # ===== INICIO APORTES CECILIA =====
    # Delimitadores
    'LKEY', 'RKEY', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'COMMA', 'SEMICOLON', 'DOT',
    # Tipos de datos
    'NUMBER', 'BIGINT', 'STRING', 'BOOLEAN', 'NULL', 'UNDEFINED',
    'IDENTIFIER',
    # ===== FIN APORTES CECILIA =====

    # ===== INICIO APORTES FIORELLA =====

    # ===== FIN APORTES FIORELLA =====
)

# Lista para registrar los errores lexicos encontrados (usada por el log)
errores_lexicos = []


# =====================================================================
# INICIO APORTE JORGE BRAVO - Comentarios

def t_COMMENT_BLOCK(t):               # comentario de bloque /* ... */
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    return t

t_COMMENT_LINE = r'//[^\n]*'          # comentario de linea // ...

# FIN APORTE JORGE BRAVO - Comentarios
# =====================================================================


# =====================================================================
# INICIO APORTE JORGE BRAVO - Operadores

t_STRICT_EQ    = r'==='     # identico

t_EQ           = r'=='      # igual
t_NEQ          = r'!='      # diferente
t_INCREMENT    = r'\+\+'    # incremento
t_DECREMENT    = r'--'      # decremento
t_PLUS_ASSIGN  = r'\+='     # asignacion aditiva
t_MINUS_ASSIGN = r'-='      # asignacion sustractiva
t_AND          = r'&&'      # AND logico
t_OR           = r'\|\|'    # OR logico

t_PLUS         = r'\+'      # suma
t_MINUS        = r'-'       # resta
t_TIMES        = r'\*'      # multiplicacion
t_DIVIDE       = r'/'       # division
t_MODULO       = r'%'       # modulo
t_ASSIGN       = r'='       # asignacion simple
t_NOT          = r'!'       # NOT logico
t_LT           = r'<'       # menor
t_GT           = r'>'       # mayor

# FIN APORTE JORGE BRAVO - Operadores
# =====================================================================


# =====================================================================
# INICIO APORTES CECILIA - Delimitadores y Tipos de datos

# Delimitadores
t_LKEY      = r'\{'
t_RKEY      = r'\}'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_COMMA     = r','
t_SEMICOLON = r';'
t_DOT       = r'\.'

# Cadenas (comillas dobles o simples); se quitan las comillas externas
def t_STRING(t):
    r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')'
    t.value = t.value[1:-1]
    return t

# BigInt: digitos seguidos de 'n' (ej. 1899n). 
def t_BIGINT(t):
    r'\d+n'
    t.value = int(t.value[:-1])
    return t

# Numeros enteros y decimales
def t_NUMBER(t):
    r'\d+\.\d+|\d+'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Identificadores y Palabras Reservadas (Booleanos, Null, Undefined)
# Usamos una función para evitar que "true" sea confundido con el nombre de una variable
def t_IDENTIFIER(t):
    r'[a-zA-Z_$][a-zA-Z0-9_$]*'
    
    # Validamos si el identificador es en realidad una palabra reservada de tipo de dato
    if t.value == 'true' or t.value == 'false':
        t.type = 'BOOLEAN'
        t.value = (t.value == 'true') # Lo convertimos a un booleano
    elif t.value == 'null':
        t.type = 'NULL'
        t.value = None
    elif t.value == 'undefined':
        t.type = 'UNDEFINED'
    # Nota: 'Symbol' generalmente se invoca como función (Symbol()), así que cae como IDENTIFIER
    
    return t

# FIN APORTES CECILIA - Delimitadores y Tipos de datos
# =====================================================================


# ---------------------------------------------------------------------
# Manejo de lineas, espacios y errores
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
    print(f"[ERROR LEXICO] Caracter ilegal '{t.value[0]}' en la linea {t.lexer.lineno}")
    t.lexer.skip(1)


# Construccion del analizador
lexer = lex.lex()
