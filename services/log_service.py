import os
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, filename='log_aggregator_service.log',
                    format='%(asctime)s :: %(levelname)s :: %(message)s')

LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "logs.json")

loaded_logs_cache = None

def _load_logs(use_cache=True):
    global loaded_logs_cache
    if use_cache and loaded_logs_cache is not None:
        return loaded_logs_cache
    
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            loaded_logs_cache = json.load(file)
            return loaded_logs_cache
    except FileNotFoundError:
        logging.error("LogFileNotFound: The log file could not be found.")
    except json.JSONDecodeError: # Fixed exception name
        logging.error("JSONDecodeError: Error decoding the log file.")
    except Exception as e:
        logging.error(f"Unexpected error in _load_logs: {e}")
    loaded_logs_cache = []
    return []

def _save_logs(logs):
    global loaded_logs_cache
    try:
        with open(LOG_FILE_PATH, 'w') as file:
            json.dump(logs, file, indent=4)
            loaded_logs_cache = logs
    except Exception as e:
        logging.error(f"Error in saving logs: {e}")

def store_log(entry):
    logs = _load_logs(use_cache=False)
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "entry": entry
    })
    _save_logs(logs)

def retrieve_logs():
    return _load_logs()

def analyze_logs():
    logs = _load_logs()
    return {"total_logs": len(logs)}

if __name__ == "__main__":
    store_log("Test log entry")
    print(retrieve_logs())
    print(analyze_logs())