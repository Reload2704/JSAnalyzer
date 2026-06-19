from ply import lex

tokens = (
    # Delimitadores
    'LKEY', 'RKEY', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 
    'COMMA', 'SEMICOLON', 'DOT',
    
    # Tipos de Datos Primitivos
    'NUMBER', 'BIGINT', 'STRING', 'BOOLEAN', 'NULL', 'UNDEFINED',
    'IDENTIFIER' # Necesario para distinguir palabras clave de nombres de variables
)

t_LKEY = r'\{'
t_RKEY = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'

# Strings (Soporta comillas dobles y simples)
def t_STRING(t):
    r'("[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')'
    # Quitamos las comillas externas para quedarnos solo con el valor
    t.value = t.value[1:-1] 
    return t

# BigInt (Números seguidos de una 'n', ej: 9007199254740991n)
def t_BIGINT(t):
    r'\d+n'
    t.value = int(t.value[:-1]) 
    return t

# Numbers (Enteros y decimales)
def t_NUMBER(t):
    r'\d+\.\d+|\d+'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
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

# Caracteres ignorados
t_ignore = ' \t\n'

def t_error(t):
    print(f"Carácter ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# --- Prueba del Analizador ---
if __name__ == '__main__':
    codigo_js = "3.14 100n 'hola mundo' true null undefined"
    
    lexer.input(codigo_js)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Tipo: {tok.type:10} | Valor: {tok.value} | Tipo Python: {type(tok.value).__name__}")