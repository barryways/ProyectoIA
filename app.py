from flask import Flask, jsonify, render_template, request, g
import time
from naive_bayes import NaiveBayes  # Assuming this is the file name where the model is defined
from filtro import cargar_textos
from sklearn.model_selection import train_test_split

# Preparación de train/test
texts_by_cat = cargar_textos()
docs, labels = [], []
for cat, lst in texts_by_cat.items():
    docs.extend(lst)
    labels.extend([cat] * len(lst))

X_train, X_test, y_train, y_test = train_test_split(
    docs, labels,
    test_size=0.2,
    random_state=42,
    stratify=labels
)

# Initialize the Flask application
app = Flask(__name__)

# Instancia y entrena el NB (o carga el .pkl)
nb = NaiveBayes(usar_modelo_guardado=False)

# Precalcula las métricas una sola vez
metrics = nb.evaluate(X_test, y_test)

# Middleware to log the start time of each request
@app.before_request
def log_route_start():
    g.start_time = time.time()  # Store the start time in the Flask `g` object
    print(f"Request started at {g.start_time}")

# Middleware to log the end time of each request and calculate elapsed time
@app.after_request
def log_route_end(response):
    route = request.endpoint  # Get the endpoint of the current request
    elapsed_time = time.time() - g.pop('start_time', None)  # Calculate elapsed time
    print(f"{route} ended after {elapsed_time:.2f} seconds")
    return response  # Return the response object

@app.route('/api/v1/analyst', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        data = request.get_json()
        # Validación básica
        if not data or 'input' not in data:
            return jsonify({'error': 'No input received'}), 400

        # Extraer texto y predecir
        texto = data['input']
        print(f"Received text: {texto}")
        categoria = nb.predictUserInput(texto)
        print(f"Prediction: {categoria}")

        # Devolver predicción + métricas
        return jsonify({
            'categoria': categoria,
            'precision': metrics['precision'],
            'recall':    metrics['recall'],
            'f1_score':  metrics['f1_score']
        }), 200

    # GET: renderiza la página
    elapsed = time.time() - g.start_time
    return render_template('analyst.html', time=f"{elapsed:.2f}")


# Entry point of the application
if __name__ == '__main__':
    NaiveBayes = NaiveBayes()  # Initialize the NaiveBayes model
    app.run(debug=True)  # Run the Flask application in debug mode



