from flask import Blueprint, request, jsonify
from services.cache_service import CacheService

def create_cache_bp(cache_service: CacheService) -> Blueprint:
    cache_bp = Blueprint("cache", __name__)

    @cache_bp.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @cache_bp.route("/cache/<key>", methods=["PUT"])
    def put_key(key: str):
        print("processing put request")
        value = request.json["value"]
        print("value from request", value)
        print("key from request", key)
        cache_service.handle_put(key, value)
        return jsonify({"status": "ok"})
    
    @cache_bp.route("/cache/<key>", methods=["GET"])
    def get_key(key: str):
        print("processing get request")
        cache_service.handle_get(key)
        return "<p>Request to /get</p>"

    
    return cache_bp

