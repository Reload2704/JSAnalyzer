# Generador de Logs - Analizador Semantico JS
# Uso: python generar_log.py [nombre] [archivo.js]
#   nombre   -> quien genera el log         (por ejemplo JorgeBravo)
#   archivo  -> prueba de la persona (.js)   (por ejemplo algoritmo_jorge.js)
# Genera: semantico-<nombre>-DD-MM-YYYY-HHhMM.txt
#
# Reutiliza el analizador lexico (lexerJS) para obtener los tokens y sobre
# ellos ejecuta el analizador semantico.

import os
import sys
from datetime import datetime

# Carpetas del proyecto
CARPETA_SCRIPT = os.path.dirname(os.path.abspath(__file__))          # .../semantico
RAIZ = os.path.dirname(CARPETA_SCRIPT)                               # .../JSAnalyzer
CARPETA_LEXICO = os.path.join(RAIZ, "lexico")
CARPETA_LOGS = os.path.join(CARPETA_SCRIPT, "logs")

# Permitir importar el lexer (vive en la carpeta lexico) y el semantico
sys.path.insert(0, CARPETA_LEXICO)
sys.path.insert(0, CARPETA_SCRIPT)

import lexerJS as lx          # noqa: E402
import semantico as sem       # noqa: E402


def resolver_archivo(archivo):
    """Devuelve la ruta del .js: tal cual si existe/es absoluta;
    si no, lo busca en la carpeta lexico (donde estan los algoritmos)."""
    if os.path.isabs(archivo) or os.path.exists(archivo):
        return archivo
    ruta_lexico = os.path.join(CARPETA_LEXICO, archivo)
    if os.path.exists(ruta_lexico):
        return ruta_lexico
    return os.path.join(CARPETA_SCRIPT, archivo)


def analizar_archivo(archivo):
    """Corre lexer + semantico sobre un .js y devuelve (tokens, errores)."""
    archivo = resolver_archivo(archivo)
    with open(archivo, encoding="utf-8") as f:
        codigo = f.read()

    lx.errores_lexicos.clear()
    lx.lexer.lineno = 1
    lx.lexer.input(codigo)
    tokens = list(lx.lexer)

    errores = sem.analizar(tokens)
    return archivo, tokens, errores


def generar_log(nombre, archivo):
    archivo, tokens, errores = analizar_archivo(archivo)

    ahora = datetime.now()
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    nombre_archivo_log = "semantico-{}-{}.txt".format(
        nombre, ahora.strftime("%d-%m-%Y-%Hh%M")
    )
    nombre_log = os.path.join(CARPETA_LOGS, nombre_archivo_log)

    with open(nombre_log, "w", encoding="utf-8") as log:
        log.write("LOG ANALISIS SEMANTICO - archivo: {}\n".format(archivo))
        log.write("Generado por: {}\n".format(nombre))
        log.write("Fecha: {}\n".format(ahora.strftime("%d-%m-%Y %H:%M:%S")))
        log.write("Tokens analizados: {}  |  Errores semanticos: {}\n".format(
            len(tokens), len(errores)))
        log.write("-" * 55 + "\n")
        if errores:
            log.write("ERRORES SEMANTICOS:\n")
            for e in errores:
                log.write("{}\n".format(e))
        else:
            log.write("Sin errores semanticos.\n")

    print("Log generado:", nombre_log)
    return nombre_log
