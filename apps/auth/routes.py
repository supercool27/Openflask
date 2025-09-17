from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
import datetime

auth_bp = Blueprint("auth", __name__)

# Dummy user data (production me database hoga)
USERS = {
    "manoj": "password123",
    "abita": "mypassword"
}

# Guest login
@auth_bp.route("/api/auth/guest", methods=["POST"])
def guest_login():
    token = create_access_token(
        identity="guest",
        expires_delta=datetime.timedelta(hours=1)
    )
    return jsonify({
        "status": "ok",
        "access_token": token
    }), 200


# Normal login with username & password
@auth_bp.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    if username in USERS and USERS[username] == password:
        token = create_access_token(
            identity=username,
            expires_delta=datetime.timedelta(hours=1)
        )
        return jsonify({
            "status": "ok",
            "access_token": token
        }), 200
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401


# Protected route example
@auth_bp.route("/api/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({
        "status": "ok",
        "message": f"Hello {current_user}, you accessed a protected route!"
    }), 200
