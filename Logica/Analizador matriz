from collections import defaultdict

class AnalizadorTextos:
    
    def __init__(self):
        self.vocabulario = {} # Diccionario para mapear palabra -> indice
        self.palabras = [] # Lista para mapear indice -> palabra
        self.siguiente_indice = 0
    
    def _construir_vocabulario(self, documentos):
        """
        Crea un vocabulario único a partir de todos los documentos.
        Esto define las "columnas" de nuestra matriz.
        Usa un diccionario (self.vocabulario) para eficiencia.
        """
        palabras_unicas = set()
        for doc in documentos:
            # Tokenización simple: dividir por espacio y quitar puntuación
            tokens = doc.lower().replace('.', '').replace(',', '').split()
            palabras_unicas.update(tokens)
            
        # Asignamos un índice a cada palabra única
        for palabra in sorted(list(palabras_unicas)):
            if palabra not in self.vocabulario:
                self.vocabulario[palabra] = self.siguiente_indice
                self.palabras.append(palabra)
                self.siguiente_indice += 1
                
    def construir_matriz_dispersa_dok(self, documentos):
        """
        Construye la Matriz Dispersa de Término-Documento.
        
        Esta es la 5. ESTRUCTURA DE MATRIZ DISPERSA.
        
        Usaremos la implementación "Dictionary of Keys" (DOK),
        que es, en sí misma, un DICICONARIO.
        
        Las claves son tuplas (fila, columna) o (doc_id, palabra_id).
        El valor es el conteo (frecuencia) de esa palabra en ese documento.
        """
        self._construir_vocabulario(documentos)
        
        # DOK: Dictionary of Keys
        # Es un diccionario donde la clave es (fila, columna)
        # y el valor es el dato en esa celda.
        # Es ideal para construir la matriz.
        matriz_dispersa_dok = defaultdict(int)
        
        for doc_id, doc in enumerate(documentos):
            tokens = doc.lower().replace('.', '').replace(',', '').split()
            for palabra in tokens:
                if palabra in self.vocabulario:
                    palabra_id = self.vocabulario[palabra]
                    
                    # (fila, columna) = (doc_id, palabra_id)
                    # Incrementamos el contador para esa celda
                    matriz_dispersa_dok[(doc_id, palabra_id)] += 1
                    
        return matriz_dispersa_dok

    def imprimir_matriz(self, matriz_dok, documentos):
        """
        Una forma visual de 'ver' la matriz dispersa.
        """
        print("=" * 30)
        print("MATRIZ DISPERSA TÉRMINO-DOCUMENTO")
        print("=" * 30)
        print(f"Dimensiones: {len(documentos)} Documentos x {len(self.vocabulario)} Palabras Únicas")
        print("Representación 'Dictionary of Keys' (DOK):")
        print("Formato: (ID_Documento, ID_Palabra): Conteo\n")
        
        for (doc_id, palabra_id), conteo in matriz_dok.items():
            palabra = self.palabras[palabra_id]
            print(f"  (Doc {doc_id}, Palabra '{palabra}' (id:{palabra_id})): {conteo}")
            
        print("\nRepresentación 'Densa' (solo para visualización):")
        
        # Header (Palabras)
        header = "          | " + " | ".join([f"{p[:5]:<5}" for p in self.palabras])
        print(header)
        print("-" * len(header))
        
        # Filas (Documentos)
        for doc_id in range(len(documentos)):
            fila_str = f"Doc {doc_id:<6} | "
            for palabra_id in range(len(self.palabras)):
                conteo = matriz_dok.get((doc_id, palabra_id), 0)
                fila_str += f" {conteo:<5} | "
            print(fila_str)
        print("=" * 30)