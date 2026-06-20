# Generador de Logs - Analizador Lexico JS
# Uso: python generar_log.py [nombre] [archivo.js]
#   nombre   -> quien genera el log         (por ejemplo JorgeBravo)
#   archivo  -> prueba de la persona (.js)   (por ejemplo algoritmo_jorge.js)
# Genera: lexico-<nombre>-DD-MM-YYYY-HHhMM.txt

import os
import sys
from datetime import datetime
import lexerJS as lx

# Carpeta donde se guardan todos los logs (junto a este script)
CARPETA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")


def generar_log(nombre, archivo):
    with open(archivo, encoding="utf-8") as f:
        codigo = f.read()

    # Ejecutar el analizador
    lx.errores_lexicos.clear()
    lx.lexer.lineno = 1
    lx.lexer.input(codigo)
    tokens = list(lx.lexer)
    errores = lx.errores_lexicos

    # Nombre del log: lexico-nombre-fecha-hora.txt (dentro de la carpeta logs)
    ahora = datetime.now()
    os.makedirs(CARPETA_LOGS, exist_ok=True)
    nombre_archivo_log = "lexico-{}-{}.txt".format(nombre, ahora.strftime("%d-%m-%Y-%Hh%M"))
    nombre_log = os.path.join(CARPETA_LOGS, nombre_archivo_log)

    # Escribir el log
    with open(nombre_log, "w", encoding="utf-8") as log:
        log.write("LOG ANALISIS LEXICO - archivo: {}\n".format(archivo))
        log.write("Generado por: {}\n".format(nombre))
        log.write("Fecha: {}\n".format(ahora.strftime("%d-%m-%Y %H:%M:%S")))
        log.write("Tokens reconocidos: {}  |  Errores: {}\n".format(len(tokens), len(errores)))
        log.write("-" * 55 + "\n")
        for t in tokens:
            log.write("Linea {:<3} | {:<12} | {!r}\n".format(t.lineno, t.type, t.value))
        if errores:
            log.write("-" * 55 + "\n")
            log.write("ERRORES LEXICOS:\n")
            for e in errores:
                log.write("Linea {}: caracter ilegal {!r}\n".format(e["linea"], e["caracter"]))

    print("Log generado:", nombre_log)
    return nombre_log

