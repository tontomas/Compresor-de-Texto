import heapq
from collections import Counter
import pickle # <-- NECESARIO para guardar/cargar el diccionario (metadata)

# 1. ESTRUCTURA DE ÁRBOL
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol(texto):
    frecuencias = Counter(texto)
    cola_prioridad = []
    for caracter, frecuencia in frecuencias.items():
        heapq.heappush(cola_prioridad, NodoHuffman(caracter, frecuencia))
        
    while len(cola_prioridad) > 1:
        nodo_izq = heapq.heappop(cola_prioridad)
        nodo_der = heapq.heappop(cola_prioridad)
        frecuencia_fusionada = nodo_izq.frecuencia + nodo_der.frecuencia
        nodo_fusionado = NodoHuffman(None, frecuencia_fusionada)
        nodo_fusionado.izquierda = nodo_izq
        nodo_fusionado.derecha = nodo_der
        heapq.heappush(cola_prioridad, nodo_fusionado)
        
    if len(cola_prioridad) == 1:
        return cola_prioridad[0]
    return None

def _generar_codigos_recursivo(nodo, codigo_actual, mapa_codigos):
    if nodo is None:
        return
    if nodo.caracter is not None:
        mapa_codigos[nodo.caracter] = codigo_actual or "0"
        return
    _generar_codigos_recursivo(nodo.izquierda, codigo_actual + "0", mapa_codigos)
    _generar_codigos_recursivo(nodo.derecha, codigo_actual + "1", mapa_codigos)

def generar_mapa_codigos(raiz_arbol):
    mapa_codigos = {}
    if raiz_arbol is not None:
        _generar_codigos_recursivo(raiz_arbol, "", mapa_codigos)
    return mapa_codigos

# --- FUNCIONES BINARIAS DE PERSISTENCIA (Añadidas) ---

def _cadena_a_bytes(bits_cadena):
    """Convierte una cadena de '0's y '1's en un objeto de bytes."""
    bytes_array = bytearray()
    
    extra_bits = len(bits_cadena) % 8
    padding = 0
    if extra_bits != 0:
        padding = 8 - extra_bits
        bits_cadena += '0' * padding

    for i in range(0, len(bits_cadena), 8):
        byte_segmento = bits_cadena[i:i+8]
        entero = int(byte_segmento, 2)
        bytes_array.append(entero)
        
    return bytes(bytes_array), padding

def guardar_binario(datos_binarios, nombre_archivo, padding, mapa_codigos):
    """Guarda datos comprimidos, padding y el mapa de códigos."""
    try:
        # Serializamos el mapa de códigos y el padding
        meta_data = {
            'padding': padding,
            'mapa_codigos': mapa_codigos
        }
        
        with open(nombre_archivo, 'wb') as f:
            pickle.dump(meta_data, f) # Guarda el diccionario necesario para descomprimir
            f.write(datos_binarios)
        return True
    except Exception as e:
        print(f"Error guardando binario: {e}")
        return False
    
def cargar_binario(nombre_archivo):
    """Carga los bytes comprimidos y la metadata (diccionario) del archivo."""
    try:        
        with open(nombre_archivo, 'rb') as f: # 'rb' = read binary
            # Cargamos el diccionario y el padding primero
            meta_data = pickle.load(f)
            padding = meta_data['padding']
            mapa_codigos = meta_data['mapa_codigos']
            datos_comprimidos = f.read()
            
        bits_cadena = ""
        for byte_data in datos_comprimidos:
            # Convierte cada byte a su representación de 8 bits
            bits_cadena += format(byte_data, '08b')
            
        if padding > 0:
            bits_cadena = bits_cadena[:-padding]
            
        # Devolvemos la cadena de bits y el diccionario (el árbol no es necesario)
        return bits_cadena, mapa_codigos
        
    except Exception as e:
        print(f"Error cargando binario: {e}")
        return None, None

# --- Función de Descompresión INDEPENDIENTE (Añadida) ---

def descomprimir_mapa(texto_comprimido_bits, mapa_codigos):
    """
    Descomprime usando el mapa de códigos, haciendo el proceso independiente
    del árbol.
    """
    if not texto_comprimido_bits or not mapa_codigos:
        return ""
    
    # Creamos el mapa inverso: código -> caracter
    mapa_inverso = {v: k for k, v in mapa_codigos.items()}
    
    texto_descomprimido = ""
    codigo_actual = ""
    
    for bit in texto_comprimido_bits:
        codigo_actual += bit
        
        if codigo_actual in mapa_inverso:
            caracter = mapa_inverso[codigo_actual]
            texto_descomprimido += caracter
            codigo_actual = "" # Reiniciamos para el siguiente código
            
    return texto_descomprimido

# --- Funciones de Interfaz (Modificadas) ---

def comprimir(texto):
    """
    Comprime el texto.
    """
    if not texto:
        return b"", 0, {}

    raiz_arbol = construir_arbol(texto)
    mapa_codigos = generar_mapa_codigos(raiz_arbol)
    
    texto_comprimido_bits = "".join(mapa_codigos.get(caracter, "") for caracter in texto)
        
    # Compresión real: convertimos la cadena de bits a bytes
    datos_binarios, padding = _cadena_a_bytes(texto_comprimido_bits)

    return datos_binarios, padding, mapa_codigos

# Eliminamos la antigua función descomprimir basada en árbol.
# def descomprimir(texto_comprimido, raiz_arbol):
#    ...