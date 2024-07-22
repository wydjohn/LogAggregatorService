import os
from datetime import datetime
import json

LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "logs.json")

def _load_logs():
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            logs = json.load(file)
    except FileNotFoundError:
        logs = []
    except json.JSONDecodeError:
        logs = []
    return logs

def _save_logs(logs):
    with open(LOG_FILE_PATH, 'w') as file:
        json.dump(logs, file, indent=4)

def store_log(entry):
    logs = _load_logs()
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "entry": entry
    })
    _save_msgs(logs)

def retrieve_logs():
    return _load_logs()

def analyze_logs():
    logs = _load_logs()
    return {"total_logs": len(logs)}