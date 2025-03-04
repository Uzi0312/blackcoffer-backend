import json
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app import db  # ✅ Import db from app.py

bp = Blueprint('flasksetup', __name__)  # ✅ Use a Blueprint

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    end_year = db.Column(db.String(10))
    intensity = db.Column(db.Integer)
    sector = db.Column(db.String(255))
    topic = db.Column(db.String(255))

@bp.route('/data', methods=['GET'])
def get_data():
    filters = {}
    for key in ['country', 'region', 'topic', 'sector']:
        if request.args.get(key):
            filters[key] = request.args.get(key)

    query = DataPoint.query.filter_by(**filters).all()
    result = [{column.name: getattr(data, column.name) for column in data.__table__.columns} for data in query]

    return jsonify(result)

@bp.route('/load_data', methods=['POST'])
def load_data():
    try:
        with open('jsondata.json', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            record = DataPoint(
                end_year=item.get("end_year", ""),
                intensity=int(item["intensity"]) if item.get("intensity") not in [None, ""] else None,
                sector=item.get("sector", ""),
                topic=item.get("topic", "")
            )
            db.session.add(record)

        db.session.commit()
        return jsonify({'message': 'Data loaded successfully'})

    except Exception as e:
        return jsonify({'error': str(e)})
