from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import gc  # Garbage collector

load_dotenv()

app = Flask(__name__)

logs = []

@app.route('/')
def home():
    return "Welcome to the LogAggregatorService!"

@app.route('/submit', methods=['POST'])
def submit_log():
    log_data = request.get_json()
    logs.append(log_data)
    return jsonify({"message": "Log submitted successfully.", "data": log_request_data}), 200

@app.route('/logs', methods=['GET'])
def view_logs():
    log_slice = logs[-10:]
    return jsonify({"message": "Logs fetched successfully.", "logs": log_slice}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", default="False").lower() in ['true', '1', 't'], 
            host=os.getenv("HOST", default="0.0.0.0"), 
            port=int(os.getenv("PORT", 5000)))