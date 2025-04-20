from collections import defaultdict
from filtro import cargar_textos
from pathlib import Path
import re
from collections import defaultdict
import math
import unicodedata
import pickle



class NaiveBayes:
    def __init__(self, usar_modelo_guardado=True):
        if usar_modelo_guardado and Path("modelo_naive_bayes.pkl").exists():
            print("Cargando modelo desde archivo...")
            with open("modelo_naive_bayes.pkl", "rb") as f:
                self.modelo = pickle.load(f)
            print("Modelo cargado desde archivo")
        else:
            self.textos_por_categoria = cargar_textos()
            self.X = [
                self.textos_por_categoria["business"],
                self.textos_por_categoria["entertainment"],
                self.textos_por_categoria["politics"],
                self.textos_por_categoria["sport"],
                self.textos_por_categoria["tech"]
            ]
            self.y = ['business', 'entertainment', 'politics', 'sport', 'tech']
            print("Textos cargados a la clase")
            self.modelo = self.entrenar_naive_bayes(self.X, self.y)
            print("Modelo entrenado")
            with open("modelo_naive_bayes.pkl", "wb") as f:
                pickle.dump(self.modelo, f)
            print("Modelo guardado en archivo")

    def default_float_dict(self):
        return defaultdict(float)                                                                                                                                               
    
    def preprocesar_texto_uk(self, texto):
        if isinstance(texto, list):  # Si recibe una lista por error
            texto = ' '.join(texto)  # Convierte a string
        
        # Normalización y limpieza
        texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
        texto = re.sub(r'[^\w\s£$€\'’]', ' ', texto)  # Conserva símbolos clave
    
        # Manejo de contracciones UK
        contracciones = {
            "'s": " is", "’s": " is",
            "'re": " are", "'ll": " will",
            "n't": " not", "'d": " would"
        }
        for contr, exp in contracciones.items():
            texto = texto.replace(contr, exp)
        
        # Tokenización avanzada (conserva £, números, etc.)
        palabras = re.findall(r'£?\d+(?:\.\d+)?%?|\w+', texto.lower())
        
        # Stopwords específicas para inglés UK
        stopwords = {
            'the', 'and', 'to', 'of', 'in', 'for', 'is', 'on', 'that', 'this',
            'with', 'it', 'as', 'are', 'be', 'at', 'from', 'by', 'have', 'has'
        }
        return [p for p in palabras if p not in stopwords and len(p) > 2]

    def entrenar_naive_bayes(self, X, y):
        modelo = {
            'prior': defaultdict(float),
            'log_prob': defaultdict(self.default_float_dict),  # <- cambiado
            'vocabulario': set(),
            'total_palabras': defaultdict(int)
        }
        
        # Aplanar X si es una lista de listas
        documentos = []
        etiquetas = []
        for categoria, docs in zip(y, X):
            if isinstance(docs, list):
                documentos.extend(docs)
                etiquetas.extend([categoria] * len(docs))
            else:
                documentos.append(docs)
                etiquetas.append(categoria)
        
        # Construcción del modelo
        for doc, clase in zip(documentos, etiquetas):
            palabras = self.preprocesar_texto_uk(doc)
            modelo['total_palabras'][clase] += len(palabras)
            for p in palabras:
                modelo['log_prob'][clase][p] += 1
                modelo['vocabulario'].add(p)
        
        # Suavizado Laplace y log-probs
        tam_vocab = len(modelo['vocabulario'])
        for clase in modelo['log_prob']:
            total = modelo['total_palabras'][clase]
            modelo['prior'][clase] = math.log(sum(1 for c in etiquetas if c == clase) / len(etiquetas))
            
            for palabra in modelo['vocabulario']:
                count = modelo['log_prob'][clase].get(palabra, 0) + 1
                modelo['log_prob'][clase][palabra] = math.log(count / (total + tam_vocab))
        
        return modelo

    def predecir(self, modelo, texto):
        palabras = self.preprocesar_texto_uk(texto)
        scores = {clase: modelo['prior'][clase] for clase in modelo['prior']}
        
        for clase in scores:
            for palabra in palabras:
                if palabra in modelo['vocabulario']:
                    scores[clase] += modelo['log_prob'][clase].get(palabra, 
                        math.log(1 / (modelo['total_palabras'][clase] + len(modelo['vocabulario']))))
        
        return max(scores.items(), key=lambda x: x[1])[0]

    def leer_archivo_especifico():
        ruta = Path(__file__).parent / ".." / "BBC News Summary"  / "Summaries" / "politics" / "406.txt"
        ruta = ruta.resolve()  # Convierte la ruta a absoluta
    
        try:
            with open(ruta, "r", encoding="latin-1") as f:
                texto = f.read()
            return texto
        except Exception as e:
            return f"Error al leer el archivo: {e}"
    
    def predictUserInput(self, userInput):
        print("Texto recibido por la clase: ", userInput)
        nueva_entrada = ['']
        nueva_entrada.append(userInput)
        prediccion = self.predecir(self.modelo, userInput)
        print("Que noticia es ? ", prediccion)
       
       
        if(prediccion == 'business'):
            prediccion = 'negocios'
        elif(prediccion == 'entertainment'):
            prediccion = 'entretenimiento'
        elif(prediccion == 'politics'):
            prediccion = 'politica'
        elif(prediccion == 'sport'):
            prediccion = 'deportes'
        elif(prediccion == 'tech'):
            prediccion = 'tecnologia'
        else:
            prediccion = 'No se ha podido clasificar la noticia'
        return prediccion