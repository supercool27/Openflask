from flask import Blueprint, jsonify, request

health_bp = Blueprint('health', __name__)

CURRENT_APP_VERSION = "1.0.0"

@health_bp.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "Server is running"
    }), 200

@health_bp.route("/api/version", methods=["GET"])
def version_check():
    client_version = request.args.get("version")
    if not client_version:
        return jsonify({
            "status": "error",
            "message": "Version parameter missing"
        }), 400

    if client_version == CURRENT_APP_VERSION:
        return jsonify({
            "status": "ok",
            "update_required": False,
            "message": "Version is up to date"
        }), 200
    else:
        return jsonify({
            "status": "ok",
            "update_required": True,
            "latest_version": CURRENT_APP_VERSION,
            "message": "Please update your app"
        }), 200
