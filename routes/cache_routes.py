from flask import Blueprint, request, jsonify
from services import cache_service
from services import routing_service
from cache.local_cache import LocalCache

cache_bp = Blueprint("cache", __name__)

local_cache = LocalCache()
routing_service = routing_service


@cache_bp.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@cache_bp.route("/cache/<key>", methods=["PUT"])
def put_key(key):
    print("processing request")
    value = request.json["value"]
    print("value from request", value)
    print("key from request", key)
    handle_put(key, value)
    return jsonify({"status": "ok"})

# @cache_bp.route("/cache/<key>", methods=["GET"])
# def get_key(key):
#     routing_service.get()
#     return "<p>Request to /get</p>"
