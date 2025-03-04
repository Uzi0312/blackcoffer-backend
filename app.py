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

# ✅ Run Flask (Only in Development)
if __name__ == '__main__':
    app.run(debug=True)
