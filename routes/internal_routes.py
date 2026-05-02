from flask import Blueprint, request, jsonify
from services.cache_service import CacheService
from services.replication_service import replicate_to

def create_internal_bp(cache_service: CacheService) -> Blueprint:
    internal_bp = Blueprint("internal", __name__)

    @internal_bp.route("/internal/cache/<key>", methods=["PUT"])
    async def put_key(key: str):
        print("processing forwarded put request")
        value = request.json["value"]
        print("value from request", value)
        print("key from request", key)
        return await cache_service.handle_put(key, value)
        
    @internal_bp.route("/internal/cache/<key>", methods=["GET"])
    def get_key(key: str):
        print("processing forwarded get request")
        return cache_service.handle_get(key)
    
    @internal_bp.route("/internal/view/cache", methods=["GET"])
    def get_full_cache():
        return cache_service.handle_get_full_cache()

    @internal_bp.route("/internal/replica/<key>", methods=["PUT"])
    def put_key_replica(key: str):
        print("processing forwarded put request to replica")
        value = request.json["value"]
        print("value from request", value)
        print("key from request", key)
        return cache_service.handle_replication(key, value)

    
    return internal_bp

