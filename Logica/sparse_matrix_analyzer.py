from collections import defaultdict

class AnalizadorTextoHuffman:
    
    def __init__(self):
        self.vocabulario = {} 
        self.palabras = []    
        self.siguiente_indice = 0
    
    # *** CORRECCIÓN APLICADA AQUÍ ***
    def _construir_vocabulario(self, lista_documentos): # <-- Renombrada para claridad
        """Crea un vocabulario único a partir de los documentos."""
        palabras_unicas = set()
        
        # Iteramos sobre la lista de documentos (incluso si solo hay uno)
        for documento_unico in lista_documentos: 
            # El objeto 'documento_unico' AHORA sí es la cadena de texto
            tokens = documento_unico.lower().replace('.', '').replace(',', '').replace('\n', ' ').split()
            palabras_unicas.update(tokens)
            
        for palabra in sorted(list(palabras_unicas)):
            if palabra and palabra not in self.vocabulario:
                self.vocabulario[palabra] = self.siguiente_indice
                self.palabras.append(palabra)
                self.siguiente_indice += 1
                
    # *** CORRECCIÓN APLICADA AQUÍ ***
    def construir_matriz_dispersa_dok(self, lista_documentos): # <-- Renombrada para claridad
        """
        Construye la Matriz Dispersa de Término-Documento (N Filas x N Columnas).
        """
        # La función _construir_vocabulario ahora acepta la lista de documentos
        self._construir_vocabulario(lista_documentos)
        
        matriz_dispersa_dok = defaultdict(int)
        
        for doc_id, doc in enumerate(lista_documentos): # <-- Iteramos correctamente sobre la lista
            tokens = doc.lower().replace('.', '').replace(',', '').replace('\n', ' ').split()
            
            for palabra in tokens:
                if palabra in self.vocabulario:
                    palabra_id = self.vocabulario[palabra]
                    matriz_dispersa_dok[(doc_id, palabra_id)] += 1
                    
        return matriz_dispersa_dok

    def obtener_top_frecuencias(self, matriz_dok, top_n=25):
        """
        Convierte la matriz DOK en un diccionario de conteo y retorna las N más frecuentes.
        """
        conteo_palabras = {}
        # Asumimos que es un solo documento (doc_id=0) para fines de esta demo
        for (doc_id, palabra_id), conteo in matriz_dok.items(): 
            palabra = self.palabras[palabra_id]
            conteo_palabras[palabra] = conteo
            
        top_frecuencias = sorted(conteo_palabras.items(), key=lambda item: item[1], reverse=True)[:top_n]
        
        return top_frecuencias