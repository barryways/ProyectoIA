from flask import Flask, jsonify, render_template, request, g
import time

app = Flask(__name__)

@app.before_request
def log_route_start():
    g.start_time = time.time()
    
@app.after_request
def log_route_end(response):
    route = request.endpoint
    elapsed_time = time.time() - g.pop('start_time', None)
    print(f"{route} ended after {elapsed_time:.2f} seconds")
    return response

@app.route('/api/v1/analyst', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        data = request.get_json()# This is the received text from the imput field
        response = {'message': 'Data received', 'data': data}
        return jsonify(response), 200
    else:  # Handle GET request
        time.sleep(0.5)
        elapsed_time = time.time() - g.start_time
        return render_template('analyst.html', time=f"{elapsed_time:.2f}")

if __name__ == '__main__':
    app.run(debug=True)