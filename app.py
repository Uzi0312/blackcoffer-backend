from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# ✅ Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend (Angular) to access API

# ✅ Securely Load Database URL (from Environment Variables)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://uzair:reYXhN0QHMIzUDYEqi8CFDaW6sZnkUPL@dpg-cv3l6u8fnakc73fvp7vg-a.oregon-postgres.render.com/blackcofferdb')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def check_and_add_column():
    with app.app_context():
        inspector = inspect(db.engine)
        columns = [col["name"] for col in inspector.get_columns("data_point")]

        if "insight" not in columns:
            with db.engine.connect() as connection:
                connection.execute(text("ALTER TABLE data_point ADD COLUMN insight TEXT"))
                connection.commit()
            print("✅ 'insight' column added successfully!")

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
