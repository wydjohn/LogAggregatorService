import os
from dotenv import load_dotenv

load_dotenv()

class LogAggregatorService:
    def __init__(self, db_connection_string, queue_url):
        self.db_connection_string = db_connection_string
        self.queue_url = queue_url

    def start(self):
        print("Starting LogAggregatorService")
        self.connect_to_database()
        self.connect_to_queue()
        print("LogAggregatorService Started Successfully!")

    def connect_to_database(self):
        print(f"Connecting to database with connection string: {self.db_connection_string}")

    def connect_to_queue(self):
        print(f"Connecting to queue with URL: {self.queue_url}")

if __name__ == "__main__":
    db_connection_string = os.environ.get('DB_CONNECTION_STRING')
    queue_url = os.environ.get('QUEUE_URL')
    service = LogAggregatorService(db_connection_string, queue_url)
    service.start()