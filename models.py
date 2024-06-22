from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from datetime import datetime
import os

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

    def to_dict(self):
        """Utility method to convert a LogEntry object to a dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'log_level': self.log_level,
            'source': self.source,
            'message': self.message
        }

@app.route('/logs', methods=['POST'])
def add_log():
    """Endpoint to add a new log entry."""
    try:
        data = request.get_json()
        new_log = LogEntry(log_level=data['log_level'], source=data['source'], message=data['message'])
        db.session.add(new_log)
        db.session.commit()
        return jsonify(new_log.to_dict()), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/logs', methods=['GET'])
def get_logs():
    """Endpoint to get all log entries."""
    logs = LogEntry.query.all()
    return jsonify([log.to_dict() for log in logs])

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 Not found error handler."""
    return jsonify(error=str(e)), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)  # Consider setting debug to False in production environments