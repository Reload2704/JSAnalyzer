# Generador de Logs - JSAnalyzer
# Proyecto LP - ESPOL 2026 PAO II
#
# Genera logs del analisis por fase o completo:
#   fase: lexico | sintactico | semantico | completo
#
# Uso por linea de comandos:
#   python generar_logs.py <fase> <nombre> <archivo.js>
# Ejemplo:
#   python generar_logs.py semantico JorgeBravo algoritmo_jorge.js
#
# Los logs se guardan en la carpeta  logs/  con el nombre:
#   <fase>-<nombre>-DD-MM-YYYY-HHhMM.txt

import os
import sys
from datetime import datetime

RAIZ = os.path.dirname(os.path.abspath(__file__))
CARPETA_LOGS = os.path.join(RAIZ, "logs")

# Permitir importar cada modulo desde su carpeta y como paquete (lexico.lexerJS)
for sub in ("", "lexico", "sintactico", "semantico"):
    ruta = os.path.join(RAIZ, sub)
    if ruta not in sys.path:
        sys.path.insert(0, ruta)

import lexerJS as lx        # noqa: E402
import semantico as sem     # noqa: E402

FASES = ("lexico", "sintactico", "semantico", "completo")


def resolver_archivo(archivo):
    """Ubica el .js: absoluto, tal cual, o en la raiz del proyecto."""
    if os.path.isabs(archivo) or os.path.exists(archivo):
        return archivo
    ruta = os.path.join(RAIZ, archivo)
    return ruta if os.path.exists(ruta) else archivo


def _tokenizar(codigo):
    lx.errores_lexicos.clear()
    lx.lexer.lineno = 1
    lx.lexer.input(codigo)
    return list(lx.lexer)


# ------------------------------------------------------------------ fases
def fase_lexico(codigo):
    """Devuelve (tokens, errores_lexicos)."""
    tokens = _tokenizar(codigo)
    return tokens, list(lx.errores_lexicos)


def fase_sintactico(codigo):
    """Devuelve (ast, errores). El parser puede estar aun en construccion."""
    try:
        import parser as sintactico
    except Exception as e:
        return None, ["Analizador sintactico no disponible: {}".format(e)]

    if hasattr(sintactico, "parsear"):
        try:
            return sintactico.parsear(codigo)
        except Exception as e:
            return None, ["Error al ejecutar el parser: {}".format(e)]

    if getattr(sintactico, "parser", None) is not None:
        errs = getattr(sintactico, "errores_sintacticos", [])
        try:
            errs.clear()
        except Exception:
            pass
        lx.lexer.lineno = 1
        ast = sintactico.parser.parse(codigo, lexer=lx.lexer)
        return ast, list(errs)

    return None, ["El analizador sintactico aun no esta implementado (parser en construccion)."]


def fase_semantico(codigo):
    """Devuelve la lista de errores semanticos (trabaja sobre los tokens)."""
    tokens = _tokenizar(codigo)
    return list(sem.analizar(tokens))


# --------------------------------------------------------- secciones del log
def _seccion_lexico(codigo, log):
    tokens, errores = fase_lexico(codigo)
    log.write("=== ANALISIS LEXICO ===\n")
    log.write("Tokens reconocidos: {}  |  Errores lexicos: {}\n".format(
        len(tokens), len(errores)))
    for t in tokens:
        log.write("Linea {:<3} | {:<12} | {!r}\n".format(t.lineno, t.type, t.value))
    if errores:
        log.write("ERRORES LEXICOS:\n")
        for e in errores:
            log.write("Linea {}: caracter ilegal {!r}\n".format(e["linea"], e["caracter"]))
    log.write("\n")


def _seccion_sintactico(codigo, log):
    _, errores = fase_sintactico(codigo)
    log.write("=== ANALISIS SINTACTICO ===\n")
    log.write("Errores sintacticos: {}\n".format(len(errores)))
    for e in errores:
        log.write("{}\n".format(e))
    log.write("\n")


def _seccion_semantico(codigo, log):
    errores = fase_semantico(codigo)
    log.write("=== ANALISIS SEMANTICO ===\n")
    log.write("Errores semanticos: {}\n".format(len(errores)))
    if errores:
        for e in errores:
            log.write("{}\n".format(e))
    else:
        log.write("Sin errores semanticos.\n")
    log.write("\n")


_SECCIONES = {
    "lexico": _seccion_lexico,
    "sintactico": _seccion_sintactico,
    "semantico": _seccion_semantico,
}


def generar_log(fase, nombre, archivo):
    """Genera el log de la fase indicada (o 'completo') para un archivo .js."""
    fase = fase.lower()
    if fase not in FASES:
        raise ValueError("Fase invalida '{}'. Use: {}".format(fase, ", ".join(FASES)))

    archivo = resolver_archivo(archivo)
    with open(archivo, encoding="utf-8") as f:
        codigo = f.read()

    ahora = datetime.now()
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    nombre_log = os.path.join(
        CARPETA_LOGS,
        "{}-{}-{}.txt".format(fase, nombre, ahora.strftime("%d-%m-%Y-%Hh%M")),
    )

    fases = ("lexico", "sintactico", "semantico") if fase == "completo" else (fase,)

    with open(nombre_log, "w", encoding="utf-8") as log:
        log.write("LOG ANALISIS ({}) - archivo: {}\n".format(fase.upper(), archivo))
        log.write("Generado por: {}\n".format(nombre))
        log.write("Fecha: {}\n".format(ahora.strftime("%d-%m-%Y %H:%M:%S")))
        log.write("=" * 60 + "\n\n")
        for f_ in fases:
            _SECCIONES[f_](codigo, log)

    print("Log generado:", nombre_log)
    return nombre_log


if __name__ == "__main__":
    if len(sys.argv) == 4:
        generar_log(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print("Uso: python generar_logs.py <lexico|sintactico|semantico|completo> "
              "<nombre> <archivo.js>")
