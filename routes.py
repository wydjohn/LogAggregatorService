from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the LogAggregatorService!"

@app.route('/submit', methods=['POST'])
def submit_log():
    log_data = request.json
    return jsonify({"message": "Log submitted successfully.", "data": log_data}), 200

@app.route('/logs', methods=['GET'])
def view_logs():
    return jsonify({"message": "Logs fetched successfully.", "logs": []}), 200

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG", default="False"), host=os.getenv("HOST", default="0.0.0.0"), port=int(os.getenv("PORT", 5000)))