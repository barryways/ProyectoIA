from filtro import cargar_textos
from sklearn.model_selection import train_test_split
from naive_bayes import NaiveBayes

#Carga y organización de datos
texts_by_cat = cargar_textos()
docs, labels = [], []
for cat, docs_list in texts_by_cat.items():
    docs.extend(docs_list)
    labels.extend([cat] * len(docs_list))

#División en train / test (80 % train, 20 % test)
X_train, X_test, y_train, y_test = train_test_split(
    docs, labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

#Entrenamiento del modelo
nb = NaiveBayes(usar_modelo_guardado=False)

#Evalúa sobre el test set
results = nb.evaluate(X_test, y_test)

#Impresión de resultados
print("=== Métricas por categoría ===")
for cat in nb.y:
    p = results['precision'][cat]
    r = results['recall'][cat]
    f = results['f1_score'][cat]
    n = results['support'][cat]
    print(f"{cat}: Precisión={p:.2f}, Recall={r:.2f}, F1={f:.2f}  (n={n})")

print("\n=== Matriz de confusión ===")
print(results['confusion_matrix'])
