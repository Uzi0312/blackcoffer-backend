import json
from flask import Blueprint, jsonify, request
from sqlalchemy import text, inspect
from app import db  # ✅ Import db from app.py

bp = Blueprint('flasksetup', __name__)  # ✅ Use a Blueprint

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    end_year = db.Column(db.String(10))
    intensity = db.Column(db.Integer)
    sector = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    insight = db.Column(db.Text)  # ✅ Ensure this column exists
    url = db.Column(db.String(500))
    region = db.Column(db.String(255))
    start_year = db.Column(db.String(10))
    impact = db.Column(db.String(50))
    added = db.Column(db.String(50))
    published = db.Column(db.String(50))
    country = db.Column(db.String(255))
    relevance = db.Column(db.Integer)
    pestle = db.Column(db.String(255))
    source = db.Column(db.String(255))
    title = db.Column(db.Text)
    likelihood = db.Column(db.Integer)


@bp.route('/data', methods=['GET'])
def get_data():
    filters = {}
    for key in ['country', 'region', 'topic', 'sector']:
        if request.args.get(key):
            filters[key] = request.args.get(key)

    query = DataPoint.query.filter_by(**filters).all()
    result = [{column.name: getattr(data, column.name) for column in data.__table__.columns} for data in query]

    return jsonify(result)

@bp.route('/load_data', methods=['POST', 'GET'])
def load_data():
    try:
        with open('jsondata.json', encoding='utf-8') as file:
            data = json.load(file)

        print(f"📂 Loaded {len(data)} records from JSON")

        for item in data:
            record = DataPoint(
                end_year=item.get("end_year") or None,  # Convert empty to None
                intensity=int(item["intensity"]) if str(item.get("intensity", "0")).isdigit() else None,
                sector=item.get("sector") or None,
                topic=item.get("topic") or None,
                insight=item.get("insight") or None,
                url=item.get("url") or None,
                region=item.get("region") or None,
                start_year=item.get("start_year") or None,
                impact=item.get("impact") or None,
                added=item.get("added") or None,
                published=item.get("published") or None,
                country=item.get("country") or None,
                relevance=int(item["relevance"]) if str(item.get("relevance", "0")).isdigit() else None,
                pestle=item.get("pestle") or None,
                source=item.get("source") or None,
                title=item.get("title") or None,
                likelihood=int(item["likelihood"]) if str(item.get("likelihood", "0")).isdigit() else None,
            )
            db.session.add(record)

        db.session.commit()
        print("✅ Data committed successfully!")
        return jsonify({'message': 'Data loaded successfully'})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)})
