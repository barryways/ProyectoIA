# Datos de entrenamiento (X) y etiquetas (y)
# Cada fila es un ejemplo: [feature1, feature2, ..., featureN]
# X = [
#     ['soleado', 'calor', 'alta', 'falsa'],
#     ['soleado', 'calor', 'alta', 'verdadera'],
#     ['nublado', 'calor', 'alta', 'falsa'],
#     ['lluvia', 'templado', 'alta', 'falsa'],
#     ['lluvia', 'frio', 'normal', 'falsa'],
#     ['lluvia', 'frio', 'normal', 'verdadera'],
#     ['nublado', 'frio', 'normal', 'verdadera'],
#     ['soleado', 'templado', 'alta', 'falsa'],
#     ['soleado', 'frio', 'normal', 'falsa'],
#     ['lluvia', 'templado', 'normal', 'falsa'],
#     ['soleado', 'templado', 'normal', 'verdadera'],
#     ['nublado', 'templado', 'alta', 'verdadera'],
#     ['nublado', 'calor', 'normal', 'falsa'],
#     ['lluvia', 'templado', 'alta', 'verdadera'],
# ]
from collections import defaultdict
from filtro import cargar_textos
from pathlib import Path

print("antes de sacar textos")
# X = sacarTextos()
textos_por_categoria = cargar_textos()

print("modelos ya entrenados")
X = [textos_por_categoria["business"], 
               textos_por_categoria["entertainment"], 
               textos_por_categoria["politics"],
               textos_por_categoria["sport"],
                textos_por_categoria["tech"]
            ]

# Etiquetas (sí o no jugar)
#y = ['no', 'no', 'sí', 'sí', 'sí', 'no', 'sí', 'no', 'sí', 'sí', 'sí', 'sí', 'sí', 'no']
y = ['business', 'entertainment', 'politics', 'sport', 'tech',]



def entrenar_naive_bayes(X, y):
    total = len(y)
    clases = set(y)
    modelo = {
        'prior': {},     # P(clase)
        'condicional': {}  # P(atributo|clase)
    }

    for c in clases:
        modelo['prior'][c] = y.count(c) / total
        modelo['condicional'][c] = defaultdict(lambda: defaultdict(int))

    for i, fila in enumerate(X):
        clase = y[i]
        for j, valor in enumerate(fila):
            modelo['condicional'][clase][j][valor] += 1

    # Convertimos frecuencias a probabilidades
    for clase in clases:
        for atributo_index in modelo['condicional'][clase]:
            total_clase = sum(modelo['condicional'][clase][atributo_index].values())
            for valor in modelo['condicional'][clase][atributo_index]:
                modelo['condicional'][clase][atributo_index][valor] /= total_clase

    return modelo



def predecir(modelo, entrada):
    max_prob = 0
    mejor_clase = None

    for clase in modelo['prior']:
        prob = modelo['prior'][clase]

        for i, valor in enumerate(entrada):
            prob *= modelo['condicional'][clase][i].get(valor, 1e-6)  # Suavizado

        if prob > max_prob:
            max_prob = prob
            mejor_clase = clase

    return mejor_clase



modelo = entrenar_naive_bayes(X, y)
nueva_entrada = ['']

def leer_archivo_especifico():
    ruta = Path(__file__).parent / ".." / "BBC News Summary"  / "Summaries" / "tech" / "004.txt"
    ruta = ruta.resolve()  # Convierte la ruta a absoluta
    
    try:
        with open(ruta, "r", encoding="latin-1") as f:
            texto = f.read()
        return texto
    except Exception as e:
        return f"Error al leer el archivo: {e}"
nueva_entrada.append(leer_archivo_especifico())

prediccion = predecir(modelo, nueva_entrada)
print("¿Jugar?", prediccion)