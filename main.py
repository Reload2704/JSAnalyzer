# JSAnalyzer - Menu general
# Proyecto LP - ESPOL 2026 PAO II
# Permite generar el log de una fase (lexico, sintactico, semantico) o completo.

from generar_logs import generar_log

MENU = {
    "1": "lexico",
    "2": "sintactico",
    "3": "semantico",
    "4": "completo",
}

print("=" * 50)
print("   JSAnalyzer - Analizador de JavaScript (PLY)")
print("=" * 50)
print("Seleccione la fase a analizar:")
print("  1) Lexico")
print("  2) Sintactico")
print("  3) Semantico")
print("  4) Completo (lexico + sintactico + semantico)")

opcion = input("Opcion [1-4]: ").strip()
fase = MENU.get(opcion)

if fase is None:
    print("Opcion invalida. Debe elegir 1, 2, 3 o 4.")
    raise SystemExit(1)

nombre = input("Nombre de quien genera el log: ").strip()
archivo = input("Archivo .js a analizar: ").strip()

try:
    generar_log(fase, nombre, archivo)
except FileNotFoundError:
    print("Error: no se encontro el archivo '{}'.".format(archivo))
