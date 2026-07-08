# Analizador Semantico - JavaScript (PLY)
# Proyecto LP - ESPOL 2026 PAO II
#
# Verifica que las construcciones reconocidas tengan un significado valido
# segun las reglas semanticas de JavaScript. Ante una violacion genera un
# mensaje del tipo:  Error Semantico [Linea X]: <causa>
#
# ---------------------------------------------------------------------------
# ENTRADA: lista de tokens producida por el analizador lexico (lexerJS).
# ---------------------------------------------------------------------------
# Mientras el analizador sintactico no construya el AST, las reglas trabajan
# directamente sobre el flujo de tokens del lexer (misma fuente que usa el
# generador de logs del lexico). Cada token tiene: .type, .value, .lineno.
# Cuando el parser produzca un AST, cada verificacion se puede migrar a
# recorrer el arbol sin cambiar los mensajes de error.
# ---------------------------------------------------------------------------

# =====================================================================
# INFRAESTRUCTURA COMUN (compartida por todo el grupo)
# =====================================================================

# Lista donde cada regla semantica registra los errores encontrados.
errores_semanticos = []


def registrar_error(linea, mensaje):
    """Agrega un error con el formato acordado en el documento."""
    errores_semanticos.append("Error Semantico [Linea {}]: {}".format(linea, mensaje))


class TablaSimbolos:
    """Tabla de simbolos con soporte de ambitos (scopes) anidados.

    La usan las reglas de Identificadores (Fiorella) y Asignacion de tipo
    (Cecilia). Se deja como infraestructura comun para no duplicarla.
    """

    def __init__(self):
        # pila de ambitos; el primero es el global
        self.ambitos = [{}]

    def abrir_ambito(self):
        self.ambitos.append({})

    def cerrar_ambito(self):
        if len(self.ambitos) > 1:
            self.ambitos.pop()

    def declarar(self, nombre, tipo=None, es_constante=False):
        self.ambitos[-1][nombre] = {"tipo": tipo, "constante": es_constante}

    def existe(self, nombre):
        return any(nombre in a for a in reversed(self.ambitos))

    def obtener(self, nombre):
        for a in reversed(self.ambitos):
            if nombre in a:
                return a[nombre]
        return None


def analizar(tokens):
    """Punto de entrada: ejecuta todas las reglas semanticas sobre la lista
    de tokens y devuelve la lista de errores encontrados."""
    errores_semanticos.clear()
    tabla = TablaSimbolos()

    # ----- APORTE JORGE BRAVO -----
    verificar_conversion_tipos(tokens)
    verificar_estructuras_control(tokens)

    # ----- APORTE CECILIA MONTES (pendiente) -----
    # verificar_asignacion_tipo(tokens, tabla)
    # verificar_operaciones_permitidas(tokens)

    # ----- APORTE FIORELLA QUIJANO (pendiente) -----
    # verificar_identificadores(tokens, tabla)
    # verificar_retorno_funciones(tokens)

    return errores_semanticos


# =====================================================================
# INICIO APORTE JORGE BRAVO
# Reglas: (1) Conversion de tipos   (2) Estructuras de control
# =====================================================================

# Funciones estandar de JS cuyo argumento debe poder convertirse a numero.
_FUNCIONES_A_NUMERO = ("Number", "parseInt", "parseFloat")


def _es_convertible_a_numero(texto):
    """Indica si una cadena puede convertirse a un numero (como en JS).
    Ej: "25" -> True,  "3.14" -> True,  "Hola" -> False."""
    texto = texto.strip()
    if texto == "":
        return True  # Number("") es 0 en JS
    try:
        float(texto)
        return True
    except ValueError:
        return False


def verificar_conversion_tipos(tokens):
    """REGLA 1 (Conversion de tipos): las conversiones explicitas solo son
    validas cuando el valor origen puede convertirse al tipo destino.
        Valido:   let numero = Number("25");
        Invalido: let numero = Number("Hola");

    Se detecta el patron  <Funcion> ( <cadena> )  sobre los tokens.
    """
    for i, tok in enumerate(tokens):
        if tok.type == "IDENTIFIER" and tok.value in _FUNCIONES_A_NUMERO:
            # patron esperado:  IDENTIFIER LPAREN STRING RPAREN
            if (
                i + 2 < len(tokens)
                and tokens[i + 1].type == "LPAREN"
                and tokens[i + 2].type == "STRING"
            ):
                cadena = tokens[i + 2]
                if not _es_convertible_a_numero(cadena.value):
                    registrar_error(
                        cadena.lineno,
                        "No es posible convertir el valor '{}' al tipo number.".format(
                            cadena.value
                        ),
                    )


def verificar_estructuras_control(tokens):
    """REGLA 2 (Estructuras de control): 'break' solo puede aparecer dentro
    de un bucle (while/for) o una estructura switch.
        Valido:   while (true) { break; }
        Invalido: let x = 10; break;

    Se lleva una pila de bloques '{ }'; cada bloque que abre justo despues de
    while / for / switch se marca como bloque de ciclo/switch. Un 'break' es
    valido si algun bloque abierto en la pila es de ese tipo.
    """
    pila_bloques = []       # cada elemento: True si es bloque de ciclo/switch
    proximo_es_ciclo = False

    for tok in tokens:
        if tok.type in ("WHILE", "FOR", "SWITCH"):
            proximo_es_ciclo = True

        elif tok.type == "LKEY":            # abre bloque '{'
            pila_bloques.append(proximo_es_ciclo)
            proximo_es_ciclo = False

        elif tok.type == "RKEY":            # cierra bloque '}'
            if pila_bloques:
                pila_bloques.pop()

        elif tok.type == "BREAK":
            if not any(pila_bloques):
                registrar_error(
                    tok.lineno,
                    "La instruccion 'break' solo puede utilizarse dentro de un "
                    "ciclo o una estructura switch.",
                )


# FIN APORTE JORGE BRAVO
# =====================================================================


# =====================================================================
# INICIO APORTE CECILIA MONTES
# Reglas: (1) Asignacion de tipo (const no reasignable)
#         (2) Operaciones permitidas (aritmeticas entre numericos)
# =====================================================================


# FIN APORTE CECILIA MONTES
# =====================================================================


# =====================================================================
# INICIO APORTE FIORELLA QUIJANO
# Reglas: (1) Identificadores (declaracion previa y alcance)
#         (2) Retorno de funciones
# =====================================================================



# FIN APORTE FIORELLA QUIJANO
# =====================================================================
