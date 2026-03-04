from flask import Blueprint, request, jsonify

def create_health_bp() -> Blueprint:
    health_bp = Blueprint("health", __name__)

    @health_bp.route("/ping", methods=["GET"])
    def get_ping():
        return "", 200
    
    return health_bp

