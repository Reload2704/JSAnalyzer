from generar_log import generar_log


print("=" * 45)
print("   ANALIZADOR LEXICO JS - Generador de Log")
print("=" * 45)

nombre = input("Nombre de quien genera el log: ").strip()
archivo = input("Archivo .js a analizar: ").strip()

try:
    generar_log(nombre, archivo)
except FileNotFoundError:
    print("Error: no se encontro el archivo '{}'.".format(archivo))
