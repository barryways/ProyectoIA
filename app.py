from flask import Flask, jsonify, render_template, request, g
import time
from naive_bayes import NaiveBayes  # Assuming this is the file name where the model is defined

# Initialize the Flask application
app = Flask(__name__)

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

# Define a route for the API endpoint `/api/v1/analyst`
@app.route('/api/v1/analyst', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':  # Handle POST requests
        data = request.get_json()  # Parse JSON data from the request body
        if data is None or data == {}:  # Check if no data was received
            return jsonify({'data': 'No data received'}), 400  # Return error response
        else:
            userInputText = data.get('input')  # Extract the 'input' field from the JSON data
            print(f"Received text: {userInputText}")
            # Use the NaiveBayes model to make a prediction based on the input text
            prediction = NaiveBayes.predictUserInput(userInputText)  
            response = {'message': 'Data received', 'data': prediction}  # Prepare the response
            print(f"Prediction:", prediction)
            return jsonify(response), 200  # Return the response with status code 200
    else:  # Handle GET requests
        elapsed_time = time.time() - g.start_time  # Calculate elapsed time
        # Render the `analyst.html` template and pass the elapsed time
        return render_template('analyst.html', time=f"{elapsed_time:.2f}")

# Entry point of the application
if __name__ == '__main__':
    NaiveBayes = NaiveBayes()  # Initialize the NaiveBayes model
    app.run(debug=True)  # Run the Flask application in debug mode