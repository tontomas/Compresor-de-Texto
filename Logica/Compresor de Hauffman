import heapq
from collections import defaultdict, Counter

# 1. ESTRUCTURA DE ÁRBOL
# Cada nodo en el árbol de Huffman
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    # Comparador para que el min-heap (cola de prioridad) funcione
    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

# Función principal para construir el árbol
def construir_arbol(texto):
    """
    Construye el Árbol de Huffman a partir de un texto.
    Utiliza un diccionario (Counter) y un min-heap (heapq).
    """
    
    # 2. ESTRUCTURA DE DICCIONARIO (Frecuencias)
    # Contamos la frecuencia de cada caracter
    # defaultdict(int) o Counter son implementaciones de diccionarios (mapas hash)
    frecuencias = Counter(texto)
    
    # 3. ESTRUCTURA "CASI" ÁRBOL (Min-Heap / Cola de Prioridad)
    # Creamos una cola de prioridad (min-heap) con los nodos hoja.
    # Un heap es comúnmente implementado con un array, pero conceptualmente
    # es un árbol binario completo. Es clave para este algoritmo.
    cola_prioridad = []
    for caracter, frecuencia in frecuencias.items():
        nodo = NodoHuffman(caracter, frecuencia)
        heapq.heappush(cola_prioridad, nodo)
        
    # Construimos el árbol
    while len(cola_prioridad) > 1:
        # Sacamos los dos nodos con menor frecuencia
        nodo_izq = heapq.heappop(cola_prioridad)
        nodo_der = heapq.heappop(cola_prioridad)
        
        # Creamos un nuevo nodo interno
        # El caracter es None (o un símbolo especial)
        # La frecuencia es la suma de sus hijos
        frecuencia_fusionada = nodo_izq.frecuencia + nodo_der.frecuencia
        nodo_fusionado = NodoHuffman(None, frecuencia_fusionada)
        nodo_fusionado.izquierda = nodo_izq
        nodo_fusionado.derecha = nodo_der
        
        # Agregamos el nuevo nodo a la cola
        heapq.heappush(cola_prioridad, nodo_fusionado)
        
    # El último elemento en la cola es la raíz del árbol
    return cola_prioridad[0]

# Función recursiva para generar los códigos
def _generar_codigos_recursivo(nodo, codigo_actual, mapa_codigos):
    """
    Recorre el árbol de Huffman para generar los códigos binarios.
    """
    if nodo is None:
        return
    
    # Si es un nodo hoja (tiene un caracter)
    if nodo.caracter is not None:
        mapa_codigos[nodo.caracter] = codigo_actual or "0" # Casoe special 1 solo caracter
        return

    # Recursión: 0 para la izquierda, 1 para la derecha
    _generar_codigos_recursivo(nodo.izquierda, codigo_actual + "0", mapa_codigos)
    _generar_codigos_recursivo(nodo.derecha, codigo_actual + "1", mapa_codigos)

def generar_mapa_codigos(raiz_arbol):
    """
    Función principal para generar el mapa de códigos.
    Retorna un diccionario (mapa hash).
    """
    # 4. ESTRUCTURA DE DICCIONARIO (Códigos)
    mapa_codigos = {}
    _generar_codigos_recursivo(raiz_arbol, "", mapa_codigos)
    return mapa_codigos

# Funciones principales de la interfaz
def comprimir(texto):
    """
    Comprime un texto usando el algoritmo de Huffman.
    """
    if not texto:
        return "", None, None

    raiz_arbol = construir_arbol(texto)
    mapa_codigos = generar_mapa_codigos(raiz_arbol)
    
    texto_comprimido = ""
    for caracter in texto:
        texto_comprimido += mapa_codigos[caracter]
        
    return texto_comprimido, raiz_arbol, mapa_codigos

def descomprimir(texto_comprimido, raiz_arbol):
    """
    Descomprime un texto de Huffman usando el árbol.
    """
    if not texto_comprimido or not raiz_arbol:
        return ""

    texto_descomprimido = ""
    nodo_actual = raiz_arbol
    
    # Caso especial: texto con un solo caracter repetido
    if raiz_arbol.caracter is not None:
        return raiz_arbol.caracter * raiz_arbol.frecuencia

    for bit in texto_comprimido:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
            
        # Si llegamos a un nodo hoja
        if nodo_actual.caracter is not None:
            texto_descomprimido += nodo_actual.caracter
            nodo_actual = raiz_arbol # Volvemos a la raíz
            
    return texto_descomprimido