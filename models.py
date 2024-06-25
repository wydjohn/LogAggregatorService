from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os

app = Flask(__name__)
environment = os.environ.get('FLASK_ENV', 'development')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///logaggregatorservice.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if environment == 'production':
    app.config.update(
        SQLALCHEMY_ECHO=False,
    )
else:
    app.config.update(
        DEBUG=True,
        SQLALCHEMY_ECHO=True,
    )

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
    db.session.commit()
    return jsonify(new_log.to_dict()), 201

@app.route('/logs', methods=['GET'])
def get_logs():
    logs_query = LogEntry.query
    log_level = request.args.get('log_level')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    if log_level:
        logs_query = logs_query.filter_by(log_level=log_level)
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        logs_query = logs_query.filter(LogEntry.timestamp >= start_date)
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
        logs_query = logs_query.filter(LogEntry.timestamp < end_date)
    
    logs = logs_query.paginate(page, per_page, error_out=False).items
    return jsonify([log.to_dict() for log in logs]), 200

@app.route('/logs/<int:log_id>', methods=['PUT'])
def update_log(log_id):
    log = LogEntry.query.get_or_404(log_id)
    data = request.get_json()
    log.log_level = data.get('log_level', log.log_level)
    log.source = data.get('source', log.source)
    log.message = data.get('message', log.message)
    db.session.commit()
    return jsonify(log.to_dict()), 200

@app.route('/logs/<int:log_id>', methods=['DELETE'])
def delete_log(log_id):
    log = LogEntry.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'success': True}), 204

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)