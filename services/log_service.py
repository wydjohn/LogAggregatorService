import os
import json
import logging
from datetime import datetime

# Configure basic logging
logging.basicConfig(level=logging.INFO, filename='log_aggregator_service.log',
                    format='%(asctime)s :: %(levelname)s :: %(message)s')

# Environment variable for log file path or default to 'logs.json'
LOG_FILE_PATH = os.environ.get("LOG_FILE_PATH", "logs.json")

def _load_logs():
    """Load logs from a JSON file, handle errors."""
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("LogFileNotFound: The log file could not be found.")
    except json.JSONDecodeHandler:
        logging.error("JSONDecodeError: Error decoding the log file.")
    except Exception as e:
        logging.error(f"Unexpected error in _load_logs: {e}")
    return []

def _save_logs(logs):
    """Save logs to a JSON file, handle errors."""
    try:
        with open(LOG_FILE_PATH, 'w') as file:
            json.dump(logs, file, indent=4)
    except Exception as e:
        logging.error(f"Error in saving logs: {e}")

def store_log(entry):
    """Store a new log entry."""
    logs = _load_logs()
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "entry": entry
    })
    _save_logs(logs)

def retrieve_logs():
    """Retrieve all log entries."""
    return _load_logs()

def analyze_logs():
    """Analyze logs and return total count."""
    logs = _load_logs()
    return {"total_logs": len(logs)}

if __name__ == "__main__":
    store_log("Test log entry")
    print(retrieve_logs())
    print(analyze_logs())