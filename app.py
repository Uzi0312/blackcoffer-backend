from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, inspect  
import os

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend (Angular) to access API

# ✅ Securely Load Database URL (from Environment Variables)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://uzair:reYXhN0QHMIzUDYEqi8CFDaW6sZnkUPL@dpg-cv3l6u8fnakc73fvp7vg-a.oregon-postgres.render.com/blackcofferdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def check_and_add_columns():
    with app.app_context():
        inspector = inspect(db.engine)
        columns = [col["name"] for col in inspector.get_columns("data_point")]

        missing_columns = {
            "insight": "TEXT",
            "url": "VARCHAR(500)",
            "region": "VARCHAR(255)",
            "start_year": "VARCHAR(10)",
            "impact": "VARCHAR(50)",
            "added": "VARCHAR(50)",
            "published": "VARCHAR(50)",
            "country": "VARCHAR(255)",
            "relevance": "INTEGER",
            "pestle": "VARCHAR(255)",
            "source": "VARCHAR(255)",
            "title": "TEXT",
            "likelihood": "INTEGER"
        }

        with db.engine.connect() as connection:
            for column, datatype in missing_columns.items():
                if column not in columns:
                    connection.execute(text(f"ALTER TABLE data_point ADD COLUMN {column} {datatype}"))
                    print(f"✅ Column '{column}' added successfully!")
            connection.commit()


check_and_add_column()  # Run before defining DataPoint model

# ✅ Import Blueprints (Routes)
from flasksetup import bp as flasksetup_bp
from auth import bp as auth_bp

# ✅ Register Blueprints (with URL Prefix)
app.register_blueprint(flasksetup_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/auth')

# ✅ Home Route (Check if API is Live)
@app.route('/')
def home():
    return "✅ Flask API is running!"

# ✅ Create tables if they don't exist
with app.app_context():
    db.create_all()  # ✅ Auto-create missing tables

# ✅ Run Flask (Only in Development)
if __name__ == '__main__':
    app.run(debug=True)
