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
    # Check if log_data is a list (batch) or a single dict (single log)
    if isinstance(log_data, list):
        logs.extend(log_data)  # Extend the list if multiple logs are submitted
        log_count = len(log_data)
        message = f"{log_chain_count} log items were submitted successfully."
    else:
        logs.append(log_data)
        log_count = 1
        message = "1 log item was submitted successfully."
    return jsonify({"message": message, "submitted_log_items_count": log_count}), 200

@app.route('/logs', methods=['GET'])
def view_logs():
    log_slice = logs[-10:]  # Send the last 10 logs (consider pagination for larger datasets)
    return jsonify({"message": "Logs fetched successfully.", "logs": log_slice}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", default="False").lower() in ['true', '1', 't'], 
            host=os.getenv("HOST", default="0.0.0.0"), 
            port=int(os.getenv("PORT", 5000)))