from flask import Blueprint
from services.cache_service import CacheService
from clients.node_client import NodeClient
from models.node import NodeData

def create_view_bp(node_map: dict[str, NodeData], cache_service: CacheService, node_client: NodeClient) -> Blueprint:
    view_bp = Blueprint("view", __name__)

    @view_bp.route("/view/cluster", methods=["GET"])
    def get_view_cluster():
        return node_map
    
    @view_bp.route("/view/cache", methods=["GET"])
    def get_view_cache():
        # Get local cache data with cache_service
        # Get other node cache data with node_client
        cache = []
        return cache


    return view_bp