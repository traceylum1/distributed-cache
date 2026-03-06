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
from cache.local_cache import LocalCache
from cache.eviction import LRU
from cache.expiration import TTL

def create_app():
    app = Flask(__name__)

    config = load_config()
    nodes = build_nodes(config)

    eviction_policy = LRU()
    expiration_policy = TTL(5)
    local_cache = LocalCache(capacity=3, eviction=eviction_policy, expiration=expiration_policy)

    cluster_service = ClusterService(nodes=nodes, failure_threshold=6)
    routing_service = RoutingService(nodes=nodes, replication_factor=3)
    node_client = NodeClient(retries=3)
    
    cache_service = CacheService(
        routing_service=routing_service, 
        node_client=node_client, 
        local_cache=local_cache
    )

    failure_detection = FailureDetection(
        cluster_service=cluster_service,
        node_client=node_client
    )
    failure_detection.start()

    cache_bp = create_cache_bp(cache_service)
    internal_bp = create_internal_bp(cache_service)
    
    app.register_blueprint(cache_bp)
    app.register_blueprint(internal_bp)

    return app, config

app, config = create_app()

if __name__ == "__main__":
    app.run(port=config.port)