from flask import Blueprint
from services.cache_service import CacheService
from clients.node_client import NodeClient
from models.node import NodeData

def create_view_bp(node_map: dict[str, NodeData], cache_service: CacheService, node_client: NodeClient) -> Blueprint:
    view_bp = Blueprint("view", __name__)

    @view_bp.route("/view/cluster", methods=["GET"])
    def get_view_cluster():
        print("/view/cluster endpoint hit")
        return node_map
    
    @view_bp.route("/view/cache", methods=["GET"])
    def get_view_cache():
        print("/view/cache endpoint hit")
        cache_data, _ = node_client.get_all_cache_data()
        local_cache_data, _ = cache_service.handle_get_full_cache()
        return {**cache_data, **local_cache_data}, 200


    return view_bp