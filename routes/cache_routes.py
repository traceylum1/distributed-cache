from flask import Blueprint, request, jsonify
from services.cache_service import handle_put

cache_bp = Blueprint("cache", __name__)

@cache_bp.route("/cache/<key>", methods=["PUT"])
def put_key(key):
    value = request.json["value"]
    handle_put(key, value)
    return jsonify({"status": "ok"})