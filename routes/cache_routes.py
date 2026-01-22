from flask import Blueprint, request, jsonify

def create_cache_bp(cache_service):
    cache_bp = Blueprint("cache", __name__)

    @cache_bp.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @cache_bp.route("/cache/<key>", methods=["PUT"])
    def put_key(key):
        print("processing request")
        value = request.json["value"]
        print("value from request", value)
        print("key from request", key)
        cache_service.handle_put(key, value)
        return jsonify({"status": "ok"})
    
    return cache_bp

# @cache_bp.route("/cache/<key>", methods=["GET"])
# def get_key(key):
#     routing_service.get()
#     return "<p>Request to /get</p>"
