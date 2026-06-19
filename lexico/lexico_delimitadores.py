from .ply import lex
from .ply import yacc

tokens = ("LKEY", 'RKEY', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON', 'DOT')

t_ignore = ' \t'

t_LKEY = r'\{'
t_RKEY = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'

t_ignore = ' \t'

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex.lex()

# --- Prueba del Analizador ---
if __name__ == '__main__':
    # Un fragmento de código JavaScript de prueba con tus delimitadores
    codigo_js = "if (matriz[0].valor == { x: 1 }) { console.log(); }"
    
    print("Analizando código fuente...")
    lexer.input(codigo_js)
    
    # Leer los tokens generados
    while True:
        tok = lexer.token()
        if not tok:
            break  # No hay más tokens
        print(tok)