from generar_log import generar_log, analizar_archivo


print("=" * 47)
print("   ANALIZADOR SEMANTICO JS - Generador de Log")
print("=" * 47)

nombre = input("Nombre de quien genera el log: ").strip()
archivo = input("Archivo .js a analizar: ").strip()

try:
    _, _, errores = analizar_archivo(archivo)
    print("-" * 47)
    if errores:
        print("Errores semanticos encontrados:")
        for e in errores:
            print("  " + e)
    else:
        print("Sin errores semanticos.")
    print("-" * 47)
    generar_log(nombre, archivo)
except FileNotFoundError:
    print("Error: no se encontro el archivo '{}'.".format(archivo))
