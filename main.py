import huffman_compressor as hf
import sparse_matrix_analyzer as sa

def demo_huffman():
    print("=" * 30)
    print("DEMO DE COMPRESIÓN HUFFMAN")
    print("=" * 30)
    
    texto_original = "hola esta es una prueba de compresion de texto con arboles de huffman"
    
    if not texto_original:
        print("El texto está vacío. Saliendo de la demo de Huffman.")
        return

    print(f"Texto Original: '{texto_original}'")
    print(f"Longitud Original: {len(texto_original) * 8} bits (asumiendo 8 bits/caracter)")
    
    texto_comprimido, arbol, mapa_codigos = hf.comprimir(texto_original)
    
    print("\nMapa de Códigos (Diccionario):")
    for char, code in sorted(mapa_codigos.items()):
        print(f"  '{char}': {code}")
        
    print(f"\nTexto Comprimido: '{texto_comprimido}'")
    print(f"Longitud Comprimida: {len(texto_comprimido)} bits")
    
    tasa_compresion = (len(texto_comprimido) / (len(texto_original) * 8)) * 100
    print(f"Tasa de Compresión: {tasa_compresion:.2f}%")
    
    texto_descomprimido = hf.descomprimir(texto_comprimido, arbol)
    print(f"\nTexto Descomprimido: '{texto_descomprimido}'")
    
    assert texto_original == texto_descomprimido
    print("\nVerificación: El texto original y el descomprimido coinciden. ¡Éxito!")

def demo_matriz_dispersa():
    # Documentos de ejemplo
    doc0 = "el perro come hueso"
    doc1 = "el gato come pescado"
    doc2 = "el perro y el gato son amigos"
    doc3 = "el hueso es del perro"
    
    documentos = [doc0, doc1, doc2, doc3]
    
    analizador = sa.AnalizadorTextos()
    matriz_dok = analizador.construir_matriz_dispersa_dok(documentos)
    
    # Imprimir la matriz (la función de impresión está en el analizador)
    analizador.imprimir_matriz(matriz_dok, documentos)

# --- Ejecución Principal ---
if __name__ == "__main__":
    demo_huffman()
    print("\n" + "=" * 50 + "\n")
    demo_matriz_dispersa()