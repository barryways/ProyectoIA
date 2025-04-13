'''
En este archivo implementmos un filtro para que pueda sacar los textos de las noticas de 
los .txt y meterlos en listas las cuales vamos a devolver y esas vamos a usar para entrenar
al modelo de datos en resumen
-Sacamos las noticias de los .txt
-Metemos cada texto en un elemento de una lista
-Hacemos lo anterior por cada categoria
-Devolvemos una lista de listas con cada una de las noticias y una lista de tipos de noticias
'''

import os
from pathlib import Path

def sacarTextos():
    ruta = Path(__file__).parent / ".." / "BBC News Summary" / "BBC News Summary" / "Summaries" / "business"
    ruta2 = Path(__file__).parent / ".." / "BBC News Summary" / "BBC News Summary" / "Summaries" / "entertainment"
    ruta3 = Path(__file__).parent / ".." / "BBC News Summary" / "BBC News Summary" / "Summaries" / "politics"
    ruta = ruta.resolve()  # Convierte la ruta a absoluta y normaliza los ".."
    ruta2 = ruta2.resolve()  # Convierte la ruta a absoluta y normaliza los ".."
    ruta3 = ruta3.resolve()  # Convierte la ruta a absoluta y normaliza los ".."
    
    
    
    print(f"Ruta intentada 1: {ruta}")
    lista_business = []
    lista_entertainment = []
    lista_politics = []
    for archivo in os.listdir(ruta):
        if archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta, archivo)
            try:
                with open(ruta_completa, "r", encoding="latin-1") as f:  # Cambiado a latin-1
                    texto = f.read()
                lista_business.append(texto) 
            except Exception as e:
                print(f"Error al leer {archivo}: {e}")
                
    print(f"Ruta intentada 2: {ruta2}")             
    for archivo in os.listdir(ruta2):
        if archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta2, archivo)
            try:
                with open(ruta_completa, "r", encoding="latin-1") as f:  # Cambiado a latin-1
                    texto = f.read()
                lista_entertainment.append(texto)
            except Exception as e:
                print(f"Error al leer {archivo}: {e}")
                
    print(f"Ruta intentada 3: {ruta3}")          
    for archivo in os.listdir(ruta3):
        if archivo.endswith(".txt"):
            ruta_completa = os.path.join(ruta3, archivo)
            try:
                with open(ruta_completa, "r", encoding="latin-1") as f:  # Cambiado a latin-1
                    texto = f.read()
                lista_politics.append(texto)
            except Exception as e:
                print(f"Error al leer {archivo}: {e}")

    lista_total = [lista_business, lista_entertainment, lista_politics]
    return lista_total


print("Hola")
lista = sacarTextos()

    