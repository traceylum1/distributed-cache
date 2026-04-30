from flask import Flask
from config import load_config
from cluster.membership import build_nodes
from services.failure_detection_service import FailureDetection
from services.cluster_service import ClusterService
from services.routing_service import RoutingService
from services.cache_service import CacheService
from clients.node_client import NodeClient
from routes.cache_routes import create_cache_bp
from routes.internal_routes import create_internal_bp
from routes.health_routes import create_health_bp
from routes.view_routes import create_view_bp
from cache.local_cache import LocalCache
from cache.eviction import LRU
from cache.expiration import TTL

def create_app():
    app = Flask(__name__)

    config = load_config()
    node_map = build_nodes(config)

    eviction_policy = LRU()
    expiration_policy = TTL(5)
    local_cache = LocalCache(capacity=3, eviction=eviction_policy, expiration=expiration_policy)

    cluster_service = ClusterService(
        node_map=node_map, 
        suspect_threshold=3, 
        failure_threshold=6
    )

    node_client = NodeClient(
        cluster_service=cluster_service, 
        retries=3
    )

    routing_service = RoutingService(
        node_map=node_map, 
        cluster_service=cluster_service, 
        replication_factor=3
    )

    cache_service = CacheService(
        routing_service=routing_service, 
        node_client=node_client, 
        local_cache=local_cache
    )

    failure_detection = FailureDetection(
        node_map=node_map,
        cluster_service=cluster_service,
        node_client=node_client
    )

    failure_detection.start()

    cache_bp = create_cache_bp(cache_service)
    internal_bp = create_internal_bp(cache_service)
    health_bp = create_health_bp()
    view_bp = create_view_bp(node_map)
    
    app.register_blueprint(cache_bp)
    app.register_blueprint(internal_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(view_bp)
    

    return app, config

app, config = create_app()

if __name__ == "__main__":
    app.run(port=config.port)