import os
from datetime import datetime
import json
import logging

logging.basicConfig(level=logging.INFO, filename='log_aggregator_service.log',
                    format='%(asctime)s :: %(levelname)s :: %(message)s')

LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "logs.json")

def _load_logs():
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            logs = json.load(file)
    except FileNotFoundError as e:
        logging.error(f"LogFileNotFound: {e}")
        logs = []
    except json.JSONDecodeError as e:
        logging.error(f"JSONDecodeError in loading logs: {e}")
        logs = []
    except Exception as e:
        logging.error(f"Unexpected error in _load_logs: {e}")
        logs = []
    return logs

def _save_logs(logs):
    try:
        with open(LOG_FILE_PATH, 'w') as file:
            json.dump(logs, file, indent=4)
    except IOError as e:
        logging.error(f"IOError in saving logs: {e}")
    except Exception as e:
        logging.error(f"Unexpected error in _save_logs: {e}")

def store_log(entry):
    try:
        logs = _load_logs()
        logs.append({
            "timestamp": datetime.now().isoformat(),
            "entry": entry
        })
        _save_logs(logs)
    except Exception as e:
        logging.error(f"Unexpected error in store_log: {e}")

def retrieve_logs():
    try:
        return _load_logs()
    except Exception as e:
        logging.error(f"Unexpected error in retrieve_logs: {e}")
        return []

def analyze_logs():
    try:
        logs = _load_logs()
        return {"total_logs": len(logs)}
    except Exception as e:
        logging.error(f"Unexpected error in analyze_logs: {e}")
        return {"total_logs": 0}

if __name__ == "__main__":
    store_log("Test log entry")
    print(retrieve_logs())
    print(analyze_logs())