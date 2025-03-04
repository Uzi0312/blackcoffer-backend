from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask import Blueprint

bp = Blueprint('auth', __name__)  # Use a Blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

CORS(app)  # Allow requests from Angular frontend

# Hardcoded credentials
USERNAME = "admin"
PASSWORD = "admin"

@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Ensure request data is JSON
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Missing credentials"}), 400  # Handle missing fields

    if data['username'] == USERNAME and data['password'] == PASSWORD:
        session['user'] = USERNAME  # Store session (not necessary for basic login)
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401  # If credentials are wrong

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # ✅ Use a different port to avoid conflicts
