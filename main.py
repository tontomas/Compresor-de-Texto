from Logica import huffman_compressor as hf
from Logica import sparse_matrix_analyzer as sa
import os

# --- Funciones Auxiliares ---

def crear_archivos_ejemplo_si_no_existen():
    """Crea el archivo 'texto_huffman.txt' si no existe."""
    if not os.path.exists("texto_huffman.txt"):
        with open("texto_huffman.txt", "w", encoding="utf-8") as f:
            f.write("Esta es una inicializacion, por favor pegue aqui su texto largo de 20 paginas.")
        print("--> Se creó 'texto_huffman.txt'. POR FAVOR, PEGAR SU TEXTO LARGO DENTRO.")

def leer_archivo(ruta):
    """Lee el contenido de un archivo de texto."""
    try:
        # Se lee sin strip() para mantener espacios en blanco/saltos de línea
        with open(ruta, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
            return contenido
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error leyendo '{ruta}': {e}")
        return None

def escribir_archivo(ruta, contenido):
    """Escribe el contenido en un archivo de texto."""
    try:
        with open(ruta, 'w', encoding='utf-8') as archivo:
            archivo.write(contenido)
        # Nota: Cambié el símbolo 'ÉXITO' por 'Exito' para evitar el mismo error de codificación si Python intenta imprimirlo
        print(f"--> Exito: Texto descomprimido guardado en '{ruta}'") 
    except Exception as e:
        print(f"Error escribiendo '{ruta}': {e}")

def obtener_tamanio_archivo(ruta):
    """Obtiene el tamaño de un archivo en bytes."""
    try:
        return os.path.getsize(ruta)
    except FileNotFoundError:
        return 0

# --- Función de Comparación de Contenido (Matriz Dispersa) ---

def comparar_frecuencias_semanticas(texto_original, texto_descomprimido, top_n=25):
    """
    Ejecuta el análisis de Matriz Dispersa para verificar la integridad semántica.
    """
    print("\n" + "=" * 80)
    # Nota: También reemplacé el carácter 'É' para prevenir problemas si no es solo el símbolo el problema
    print(f"VERIFICACION SEMANTICA DE CONTENIDO ({top_n} PALABRAS MAS FRECUENTES)") 
    print(f"(DEMOSTRACION DE LA ESTRUCTURA MATRIZ DISPERSA)")
    print("=" * 80)
    
    # Análisis del Archivo Original
    analizador_original = sa.AnalizadorTextoHuffman()
    matriz_original_dok = analizador_original.construir_matriz_dispersa_dok([texto_original])
    top_original = analizador_original.obtener_top_frecuencias(matriz_original_dok, top_n)

    # Análisis del Archivo Descomprimido
    analizador_descomprimido = sa.AnalizadorTextoHuffman()
    matriz_descomp_dok = analizador_descomprimido.construir_matriz_dispersa_dok([texto_descomprimido])
    top_descomprimido = analizador_descomprimido.obtener_top_frecuencias(matriz_descomp_dok, top_n)
    
    # --------------------------------------------------------
    # Muestra de la Comparación (Top-25)
    # --------------------------------------------------------
    
    print(f"{'No.':<4} | {'ORIGINAL (texto_huffman.txt)':<35} | {'DESCOMPRIMIDO (texto_descomp.txt)':<35} | {'COINCIDE':<8}")
    print("-" * 80)
    
    coincidencias = 0
    
    # Iterar sobre las 25 posiciones
    for i in range(top_n):
        
        # Obtener datos del original
        palabra_orig, freq_orig = top_original[i] if i < len(top_original) else ('-', 0)
        
        # Obtener datos del descomprimido
        palabra_descomp, freq_descomp = top_descomprimido[i] if i < len(top_descomprimido) else ('-', 0)
        
        # Verificación clave
        coincide_palabra = (palabra_orig == palabra_descomp) and (freq_orig == freq_descomp)
        
        # *** CORRECCIÓN DEL ERROR AQUÍ ***
        simbolo = "OK" if coincide_palabra else "FALLA"
        
        if coincide_palabra:
            coincidencias += 1
            
        linea_original = f"'{palabra_orig}': {freq_orig}"
        linea_descomp = f"'{palabra_descomp}': {freq_descomp}"

        print(f"{i + 1:<4} | {linea_original:<35} | {linea_descomp:<35} | {simbolo:<8}")


    # Conclusión semántica
    if coincidencias == top_n:
        print("\nCONCLUSION SEMANTICA: La distribucion de frecuencia de palabras es IDENTICA en el Top-25. ¡Integridad Perfecta!")
    else:
        print(f"\nCONCLUSION SEMANTICA: Se encontraron {top_n - coincidencias} diferencias en el Top-25.")


# --- Función Principal de la Demo ---

def demo_huffman():
    print("\n" + "=" * 50)
    print("DEMO DE COMPRESION HUFFMAN (Ciclo Completo: TXT -> BIN -> TXT)")
    print("=" * 50)
    
    nombre_archivo_original = "texto_huffman.txt"
    nombre_archivo_comprimido = "texto_comp.bin"
    nombre_archivo_descomprimido = "texto_descomp.txt"
    
    # 1. Lectura del Original
    texto_original = leer_archivo(nombre_archivo_original)
    # También debemos limpiar el texto original de posibles caracteres no ASCII en la muestra inicial si usamos la codificación 'charmap'
    texto_original_muestra = texto_original[:50].strip().encode('ascii', 'ignore').decode('ascii') if texto_original else ''
    
    if not texto_original:
        print("El archivo original está vacío o no existe.")
        return
    
    print(f"Texto Original (Muestra): '{texto_original_muestra}...'")
    
    # 2. Compresión y Guardado Binario
    datos_binarios, padding, mapa_codigos = hf.comprimir(texto_original)
    if not datos_binarios:
        print("Error: El texto no pudo ser comprimido.")
        return

    print(f"\nGuardando datos comprimidos en '{nombre_archivo_comprimido}' (Modo Binario)...")
    if not hf.guardar_binario(datos_binarios, nombre_archivo_comprimido, padding, mapa_codigos):
        return

    # 3. Lectura del Binario y Descompresión
    print(f"\nCargando binario y descomprimiendo a '{nombre_archivo_descomprimido}'...")
    
    texto_comprimido_cargado_bits, mapa_codigos_cargado = hf.cargar_binario(nombre_archivo_comprimido)
    
    if not texto_comprimido_cargado_bits:
        return
        
    texto_descomprimido = hf.descomprimir_mapa(texto_comprimido_cargado_bits, mapa_codigos_cargado)
    
    # 4. Guardado del Archivo Descomprimido
    escribir_archivo(nombre_archivo_descomprimido, texto_descomprimido)
    
    # 5. Verificación de Archivos y Tamaños
    tamanio_original_bytes = obtener_tamanio_archivo(nombre_archivo_original)
    tamanio_comprimido_bytes = obtener_tamanio_archivo(nombre_archivo_comprimido)
    tamanio_descomprimido_bytes = obtener_tamanio_archivo(nombre_archivo_descomprimido)
    
    print("\n" + "*" * 20 + " RESULTADOS DE TAMAÑO " + "*" * 20)
    print(f"  Tamaño Original ({nombre_archivo_original}): {tamanio_original_bytes} bytes")
    print(f"  Tamaño Comprimido ({nombre_archivo_comprimido}): {tamanio_comprimido_bytes} bytes")
    print(f"  Tamaño Descomprimido ({nombre_archivo_descomprimido}): {tamanio_descomprimido_bytes} bytes")
    
    if tamanio_original_bytes > 0 and tamanio_comprimido_bytes > 0:
        tasa_reduccion = (1 - (tamanio_comprimido_bytes / tamanio_original_bytes)) * 100
        print(f"  Tasa de Reduccion de Espacio: {tasa_reduccion:.2f}%")

    if texto_original.strip() == texto_descomprimido.strip():
        print("\nVerificacion de Contenido: ¡EXITO! El contenido original coincide con el descomprimido.")
    else:
        print("\nVerificacion de Contenido: FALLO. Los contenidos de archivo no coinciden.")
        
    # 6. INTEGRACIÓN: Ejecución del Análisis de Matriz Dispersa
    comparar_frecuencias_semanticas(texto_original, texto_descomprimido, top_n=100)


# --- Ejecución Principal ---
if __name__ == "__main__":
    crear_archivos_ejemplo_si_no_existen()
    demo_huffman()