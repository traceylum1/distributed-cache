from flask import Blueprint, request, jsonify
from services.cache_service import handle_put

cache_bp = Blueprint("cache", __name__)

@cache_bp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@cache_bp.route("/cache/<key>", methods=["PUT"])
def put_key(key):
    value = request.json["value"]
    handle_put(key, value)
    return jsonify({"status": "ok"})

# @cache_bp.route("/cache/<key>", methods=["GET"])
# def get_key(key):
#     routing_service.get()
#     return "<p>Request to /get</p>"
