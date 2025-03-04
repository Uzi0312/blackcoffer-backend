from flask import Blueprint, request, jsonify, session

bp = Blueprint('auth', __name__)  # ✅ Use a Blueprint

USERNAME = "admin"
PASSWORD = "admin"

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"message": "Missing credentials"}), 400

    if data['username'] == USERNAME and data['password'] == PASSWORD:
        session['user'] = USERNAME
        return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401
