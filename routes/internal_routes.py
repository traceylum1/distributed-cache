from flask import Blueprint, request, jsonify
from cache.local_cache import LocalCache

def create_internal_bp(local_cache: LocalCache) -> Blueprint:
    internal_bp = Blueprint("internal", __name__)

    @internal_bp.route("/internal/cache/<key>", methods=["PUT"])
    def put_key(key: str):
        print("processing internal put request")
        value = request.json["value"]
        print("value from request", value)
        print("key from request", key)
        if local_cache.put(key, value) == False:
            return "", 500
        return "", 200
        
    
    @internal_bp.route("/internal/cache/<key>", methods=["GET"])
    def get_key(key: str):
        print("processing internal get request")
        value = local_cache.get(key)
        if value == None:
            return "", 404
        return value, 200

    
    return internal_bp

