from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import subprocess

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow Angular to access this API

# Load database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:uzair123@localhost/blackcoffer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Import routes from both files
import flasksetup
import auth

# Register Blueprints (optional)
app.register_blueprint(flasksetup.bp)
app.register_blueprint(auth.bp)

# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)
