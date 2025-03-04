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

@app.route('/load_data', methods=['POST', 'GET'])
def load_data():
    try:
        with open('jsondata.json', encoding='utf-8') as file:
            data = json.load(file)

        print(f"📂 Loaded {len(data)} records from JSON")

        for item in data:
            record = DataPoint(
                end_year=item.get("end_year", None),  # Convert empty string to None
                intensity=int(item["intensity"]) if str(item.get("intensity", "")).isdigit() else None,  # ✅ Check if value is a digit
                sector=item.get("sector", ""),
                topic=item.get("topic", ""),
                insight=item.get("insight", ""),
                url=item.get("url", ""),
                region=item.get("region", ""),
                start_year=item.get("start_year", None),
                impact=item.get("impact", ""),
                added=item.get("added", ""),
                published=item.get("published", ""),
                country=item.get("country", ""),
                relevance=int(item["relevance"]) if str(item.get("relevance", "")).isdigit() else None,
                pestle=item.get("pestle", ""),
                source=item.get("source", ""),
                title=item.get("title", ""),
                likelihood=int(item["likelihood"]) if str(item.get("likelihood", "")).isdigit() else None,
            )
            db.session.add(record)

        db.session.commit()
        print("✅ Data committed successfully!")
        return jsonify({'message': 'Data loaded successfully'})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)})
