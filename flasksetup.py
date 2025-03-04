from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Import text for raw SQL execution
import json
from flask_cors import CORS
from flask import Blueprint
from app import db

bp = Blueprint('flasksetup', __name__)  # Use a Blueprint


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://uzair:reYXhN0QHMIzUDYEqi8CFDaW6sZnkUPL@dpg-cv3l6u8fnakc73fvp7vg-a/blackcofferdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

with app.app_context():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # Use text() for raw SQL
            print("✅ Connected to MySQL successfully!")
    except Exception as e:
        print(f"❌ Error connecting to MySQL: {e}")

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    end_year = db.Column(db.String(10))
    intensity = db.Column(db.Integer)
    sector = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    insight = db.Column(db.Text)
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

@app.route('/load_data', methods=['POST', 'GET'])
def load_data():
    try:
        with open(r'C:\Users\Mohammed Uzair\OneDrive\Desktop\LinkedIn Assignments\BlackCoffer\jsondata.json', encoding='utf-8') as file:
            data = json.load(file)

        print(f"📂 Loaded {len(data)} records from JSON")

        for item in data:
            record = DataPoint(
                end_year=item.get("end_year", ""),
                intensity=int(item["intensity"]) if item.get("intensity") not in [None, ""] else None,
                sector=item.get("sector", ""),
                topic=item.get("topic", ""),
                insight=item.get("insight", ""),
                url=item.get("url", ""),
                region=item.get("region", ""),
                start_year=item.get("start_year", ""),
                impact=item.get("impact", ""),
                added=item.get("added", ""),
                published=item.get("published", ""),
                country=item.get("country", ""),
                relevance=int(item["relevance"]) if item.get("relevance") not in [None, ""] else None,
                pestle=item.get("pestle", ""),
                source=item.get("source", ""),
                title=item.get("title", ""),
                likelihood=int(item["likelihood"]) if item.get("likelihood") not in [None, ""] else None,
            )
            db.session.add(record)

        db.session.commit()
        print("✅ Data committed successfully!")
        return jsonify({'message': 'Data loaded successfully'})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)})



@app.route('/data', methods=['GET'])
def get_data():
    filters = {}
    for key in ['country', 'region', 'topic', 'sector']:
        if request.args.get(key):
            filters[key] = request.args.get(key)

    query = DataPoint.query.filter_by(**filters).all()

    # Convert query results to a JSON-friendly format
    result = []
    for data in query:
        data_dict = {column.name: getattr(data, column.name) for column in data.__table__.columns}
        result.append(data_dict)

    return jsonify(result)


@app.route('/')
def home():
    return "Flask API is running!"

if __name__ == '__main__':
    CORS(app, origins=["http://localhost:4200"])
    with app.app_context():
        db.create_all()
    app.run(debug=True)
