from Logica import huffman_compressor as hf
from Logica import sparse_matrix_analyzer as sa
import os

def crear_archivos_ejemplo_si_no_existen():
    """
    Crea archivos de texto de prueba para que el programa funcione
    inmediatamente sin que el usuario tenga que crearlos manualmente.
    """
    # Archivo para Huffman
    if not os.path.exists("texto_huffman.txt"):
        with open("texto_huffman.txt", "w", encoding="utf-8") as f:
            f.write("hola esta es una prueba de compresion de texto desde un archivo txt con huffman")
        print("--> Se creó 'texto_huffman.txt' de prueba.")

    # Archivos para Matriz Dispersa
    docs = {
        "doc1.txt": "el perro come hueso en el jardin",
        "doc2.txt": "el gato come pescado en la cocina",
        "doc3.txt": "el perro y el gato son amigos en la casa",
        "doc4.txt": "el hueso es del perro y el pescado del gato"
    }
    
    for nombre, contenido in docs.items():
        if not os.path.exists(nombre):
            with open(nombre, "w", encoding="utf-8") as f:
                f.write(contenido)
            print(f"--> Se creó '{nombre}' de prueba.")

def leer_archivo(ruta):
    """
    Lee el contenido de un archivo de texto.
    Maneja errores si el archivo no existe.
    """
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read().strip() # .strip() quita espacios al inicio/final
            return contenido
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta}'.")
        return None
    except Exception as e:
        print(f"Error leyendo '{ruta}': {e}")
        return None

def demo_huffman():
    print("\n" + "=" * 40)
    print("DEMO DE COMPRESIÓN HUFFMAN (Desde Archivo)")
    print("=" * 40)
    
    nombre_archivo = "texto_huffman.txt"
    print(f"Leyendo archivo: {nombre_archivo}...")
    
    texto_original = leer_archivo(nombre_archivo)
    
    if not texto_original:
        return

    print(f"Texto Original: '{texto_original}'")
    print(f"Longitud Original: {len(texto_original) * 8} bits (asumiendo 8 bits/caracter)")
    
    texto_comprimido, arbol, mapa_codigos = hf.comprimir(texto_original)
    
    # Mostramos solo los primeros 10 códigos para no saturar si es muy largo
    print("\nMapa de Códigos (Muestra de los primeros):")
    i = 0
    for char, code in sorted(mapa_codigos.items()):
        print(f"  '{char}': {code}")
        i += 1
        if i >= 10:
            print("  ... (más caracteres ocultos)")
            break
        
    print(f"\nTexto Comprimido: '{texto_comprimido}'")
    print(f"Longitud Comprimida: {len(texto_comprimido)} bits")
    
    if len(texto_original) > 0:
        tasa_compresion = (len(texto_comprimido) / (len(texto_original) * 8)) * 100
        print(f"Tasa de Compresión: {tasa_compresion:.2f}%")
    
    texto_descomprimido = hf.descomprimir(texto_comprimido, arbol)
    
    # Verificación
    if texto_original == texto_descomprimido:
        print("\nVerificación: ¡ÉXITO! El texto descomprimido es idéntico al original.")
    else:
        print("\nVerificación: FALLÓ. Los textos no coinciden.")

def demo_matriz_dispersa():
    print("\n" + "=" * 40)
    print("DEMO MATRIZ DISPERSA (Múltiples Archivos)")
    print("=" * 40)
    
    nombres_archivos = ["doc1.txt", "doc2.txt", "doc3.txt", "doc4.txt"]
    documentos = []
    
    print("Leyendo documentos...")
    for nombre in nombres_archivos:
        contenido = leer_archivo(nombre)
        if contenido:
            documentos.append(contenido)
            print(f"  - {nombre}: Leído ({len(contenido)} caracteres)")
        else:
            print(f"  - {nombre}: Saltado (Error)")
    
    if not documentos:
        print("No hay documentos válidos para procesar.")
        return

    analizador = sa.AnalizadorTextos()
    matriz_dok = analizador.construir_matriz_dispersa_dok(documentos)
    
    # Imprimir la matriz
    analizador.imprimir_matriz(matriz_dok, documentos)

# --- Ejecución Principal ---
if __name__ == "__main__":
    # 1. Crear archivos dummy para que el usuario pueda probarlo ya mismo
    crear_archivos_ejemplo_si_no_existen()
    
    # 2. Ejecutar demos
    demo_huffman()
    demo_matriz_dispersa()