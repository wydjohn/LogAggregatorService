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
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route('/logs', methods=['POST'])
def add_log():
    data = request.get_json()
    if not data or 'log_level' not in data or 'source' not in data or 'message' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_log = LogEntry(log_level=data['log_level'], source=data['source'], message=data['message'])
    db.session.add(new_log)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    return jsonify(new_log.to_dict()), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = LogEntry.query.all()
    return jsonify([log.to_dict() for log in logs]), 200

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)