from services.routing_service import RoutingService
from clients.node_client import NodeClient
from cache.local_cache import LocalCache
class CacheService:
    def __init__(self, routing_service: RoutingService, node_client: NodeClient, local_cache: LocalCache):
        self.routing_service = routing_service
        self.node_client = node_client
        self.local_cache = local_cache

    def handle_put(self, key: str, value: str):
        node = self.routing_service.get_primary_node(key)

        if node.is_local:
            self.local_cache.put(key, value)
        else:
            res = self.node_client.forward_put(node.url, key, value)

    def handle_get(self, key: str):
        node = self.routing_service.get_primary_node(key)

        if node.is_local:
            value = self.local_cache.get(key)
        else:
            res = self.node_client.forward_get(node.url, key)