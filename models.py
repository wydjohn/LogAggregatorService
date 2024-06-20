from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from flask import Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///logaggregatorservice.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class LogEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    log_level = db.Column(db.String(20))
    source = db.Column(db.String(50))
    message = db.Column(db.Text)
    def __repr__(self):
        return f'<LogEntry {self.id} - {self.timestamp} - {self.log_level}>'
if __name__ == '__main__':
    db.create_all()