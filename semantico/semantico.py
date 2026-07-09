# Analizador Semantico - JavaScript (PLY)
# Proyecto LP - ESPOL 2026 PAO II
#
# Recorre el AST producido por el analizador sintactico (parser) y verifica
# que las construcciones tengan un significado valido segun las reglas
# semanticas de JavaScript. Ante una violacion genera un mensaje del tipo:
#     Error Semantico [Linea X]: <causa>
#
# ---------------------------------------------------------------------------
# ENTRADA: el AST (lista de nodos) devuelto por parser.parsear(codigo).
# ---------------------------------------------------------------------------
# CONVENCION DE NODOS (definida en sintactico/parser.py):
#   ('num'|'str'|'bool', valor, linea) | ('id', nombre, linea)
#   ('llamada', nombre, [args], linea) | ('impresion', obj, metodo, [args], linea)
#   ('decl', tipo, nombre, valor, linea)
#   ('binaria', op, izq, der, linea) | ('unario', op, expr, linea)
#   ('while', cond, cuerpo, linea) | ('for', init, cond, incr, cuerpo, linea)
#   ('if', cond, cuerpo, sino, linea) | ('break', linea)
#   ('funcion', nombre, [params], cuerpo, retorno, linea) | ('return', expr, linea)
#   ('array', [elems], linea) | ('acceso', nombre, indice, linea)
#   ('objeto', [(clave, valor), ...], linea)
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


def _recorrer(nodo):
    """Generador que recorre recursivamente el AST y produce cada nodo
    (cada tupla cuya primera posicion es una etiqueta de texto)."""
    if isinstance(nodo, tuple) and nodo and isinstance(nodo[0], str):
        yield nodo
        for hijo in nodo[1:]:
            yield from _recorrer(hijo)
    elif isinstance(nodo, list):
        for hijo in nodo:
            yield from _recorrer(hijo)


def analizar(ast):
    """Punto de entrada: ejecuta todas las reglas semanticas sobre el AST
    y devuelve la lista de errores encontrados."""
    errores_semanticos.clear()
    if ast is None:
        return errores_semanticos
    tabla = TablaSimbolos()

    # ----- APORTE JORGE BRAVO -----
    verificar_conversion_tipos(ast)
    verificar_estructuras_control(ast)

    # ----- APORTE CECILIA MONTES (pendiente) -----
    verificar_asignacion_tipo(ast, tabla)
    verificar_operaciones_permitidas(ast)

    # ----- APORTE FIORELLA QUIJANO (pendiente) -----
    verificar_identificadores(ast, tabla)
    #verificar_retorno_funciones(ast)

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


def verificar_conversion_tipos(ast):
    """REGLA 1 (Conversion de tipos): las conversiones explicitas solo son
    validas cuando el valor origen puede convertirse al tipo destino.
        Valido:   let numero = Number("25");
        Invalido: let numero = Number("Hola");
    Se buscan los nodos ('llamada', nombre, [args], linea).
    """
    for nodo in _recorrer(ast):
        if nodo[0] == "llamada":
            nombre, args, linea = nodo[1], nodo[2], nodo[-1]
            if nombre in _FUNCIONES_A_NUMERO and args:
                arg = args[0]
                if isinstance(arg, tuple) and arg[0] == "str":
                    valor = arg[1]
                    if not _es_convertible_a_numero(valor):
                        registrar_error(
                            linea,
                            "No es posible convertir el valor '{}' al tipo number.".format(
                                valor
                            ),
                        )


def verificar_estructuras_control(ast):
    """REGLA 2 (Estructuras de control): 'break' solo puede aparecer dentro
    de un bucle (while/for) o una estructura switch.
        Valido:   while (true) { break; }
        Invalido: let x = 10; break;
    Se recorre el arbol marcando cuando se esta dentro de un ciclo. Un 'break'
    fuera de ese contexto genera error. Las funciones reinician el contexto.
    """

    def recorrer(nodo, dentro_bucle):
        if isinstance(nodo, tuple) and nodo and isinstance(nodo[0], str):
            etiqueta = nodo[0]

            if etiqueta == "break" and not dentro_bucle:
                registrar_error(
                    nodo[-1],
                    "La instruccion 'break' solo puede utilizarse dentro de un "
                    "ciclo o una estructura switch.",
                )
                return

            if etiqueta in ("while", "for", "switch"):
                for hijo in nodo[1:]:
                    recorrer(hijo, True)
                return

            if etiqueta == "funcion":   # una funcion abre un contexto nuevo
                for hijo in nodo[1:]:
                    recorrer(hijo, False)
                return

            for hijo in nodo[1:]:
                recorrer(hijo, dentro_bucle)

        elif isinstance(nodo, list):
            for hijo in nodo:
                recorrer(hijo, dentro_bucle)

    recorrer(ast, False)


# FIN APORTE JORGE BRAVO
# =====================================================================


# =====================================================================
# INICIO APORTE CECILIA MONTES
# Reglas: (1) Asignacion de tipo (const no reasignable)
#         (2) Operaciones permitidas (aritmeticas entre numericos)
# =====================================================================

def verificar_asignacion_tipo(ast, tabla):
    for nodo in _recorrer(ast):

        if nodo[0] == "decl":

            tipo_decl = nodo[1]      # let / const / var
            nombre = nodo[2]
            valor = nodo[3]
            linea = nodo[4]

            tipo = None

            if valor is not None:

                if valor[0] == "num":
                    tipo = "number"

                elif valor[0] == "str":
                    tipo = "string"

                elif valor[0] == "bool":
                    tipo = "boolean"

                elif valor[0] == "array":
                    tipo = "array"

                elif valor[0] == "objeto":
                    tipo = "object"

            tabla.declarar(
                nombre,
                tipo,
                es_constante=(tipo_decl == "const")
            )
    
def verificar_operaciones_permitidas(ast):
     for nodo in _recorrer(ast):

        if nodo[0] != "binaria":
            continue

        operador = nodo[1]
        izquierda = nodo[2]
        derecha = nodo[3]
        linea = nodo[4]

        if operador not in ("+", "-", "*", "/", "%"):
            continue

        if izquierda[0] != "num" or derecha[0] != "num":

            registrar_error(
                linea,
                "La operación '{}' solo puede realizarse entre valores numéricos.".format(
                    operador
                )
            )


# FIN APORTE CECILIA MONTES
# =====================================================================


# =====================================================================
# INICIO APORTE FIORELLA QUIJANO
# Reglas: (1) Identificadores (declaracion previa y alcance)
#         (2) Retorno de funciones
# =====================================================================
def verificar_identificadores(ast, tabla):
    # función auxiliar para revisar el árbol paso a paso
    def revisar_nodo(nodo):
        # si el nodo está vacío o no es una tupla válida, salimos
        if type(nodo) is not tuple or len(nodo) == 0:
            return

        etiqueta = nodo[0] # Ej: 'decl', 'id', 'funcion'

        # si están declarando una variable (let, const)
        if etiqueta == "decl":
            nombre_variable = nodo[2]
            tabla.declarar(nombre_variable)
            revisar_nodo(nodo[3]) # Revisamos el valor asignado por si adentro hay más variables

        # si están usando una variable que ya existe
        elif etiqueta == "id":
            nombre_variable = nodo[1]
            linea = nodo[-1]
            #si alguien guardó este nombre antes
            if tabla.existe(nombre_variable) == False:
                registrar_error(linea, f"El identificador '{nombre_variable}' no ha sido declarado.")

        # entramos a un bloque cerrado (función, if, while)
        elif etiqueta in ["funcion", "if", "while", "for"]:
            if etiqueta == "funcion":
                tabla.declarar(nodo[1]) # Guardo el nombre de la función afuera
            
            # abro una nueva capa de memoria
            # las variables creadas aquí adentro, mueren al salir
            tabla.abrir_ambito()
            
            for hijo in nodo[1:]:
                if type(hijo) is list:
                    for sub_hijo in hijo: revisar_nodo(sub_hijo)
                else:
                    revisar_nodo(hijo)
                    
            tabla.cerrar_ambito() # Destruyo la capa de memoria al salir del bloque

        # cualquier otra instrucción (sumas, restas, impresiones)
        else:
            for hijo in nodo[1:]:
                if type(hijo) is list:
                    for sub_hijo in hijo: revisar_nodo(sub_hijo)
                else:
                    revisar_nodo(hijo)

    # arranco la revisión desde la raíz del árbol
    revisar_nodo(ast)


def verificar_retorno_funciones(ast):
    # uso la función _recorrer del equipo para buscar en todo el archivo
    for nodo in _recorrer(ast):
        
        # me detengo solo cuando encuentro la definición de una función
        if nodo[0] == "funcion":
            cuerpo_funcion = nodo[3]
            tipo_prometido = nodo[4] 
            
            # ahora busco los return dentro de esta función
            for sub_nodo in _recorrer(cuerpo_funcion):
                if sub_nodo[0] == "return":
                    valor_retornado = sub_nodo[1] 
                    linea = sub_nodo[2]
                    
                    tipo_real = None
                    # averiguo el tipo de dato real que están intentando devolver
                    if type(valor_retornado) is tuple:
                        etiqueta_valor = valor_retornado[0]
                        if etiqueta_valor == "num": tipo_real = "number"
                        elif etiqueta_valor == "str": tipo_real = "string"
                        elif etiqueta_valor == "bool": tipo_real = "boolean"
                        
                    # si ambos existen y no son iguales, lanzo el error
                    if tipo_prometido != None and tipo_real != None:
                        if tipo_prometido != tipo_real:
                            registrar_error(linea, "El valor retornado no coincide con el tipo esperado.")


# FIN APORTE FIORELLA QUIJANO
# =====================================================================
