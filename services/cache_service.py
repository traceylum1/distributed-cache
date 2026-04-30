from services.routing_service import RoutingService
from clients.node_client import NodeClient
from cache.local_cache import LocalCache
from services.replication_service import replicate_to

class CacheService:
    def __init__(self, routing_service: RoutingService, node_client: NodeClient, local_cache: LocalCache):
        self.routing_service = routing_service
        self.node_client = node_client
        self.local_cache = local_cache

    async def handle_put(self, key: str, value: str):
        nodes = self.routing_service.get_primary_and_replica_nodes(key)

        primary = nodes[0]
        replicas = nodes[1:]
        print(primary)

        if primary.is_local:
            if self.local_cache.put(key, value) == False:
                return "", 500
            await replicate_to(self.node_client, replicas, key, value)
            return "", 200

        else:
            return self.node_client.forward_put(primary.url, key, value)

    def handle_get(self, key: str):
        nodes = self.routing_service.get_primary_and_replica_nodes(key)

        primary = nodes[0]

        if primary.is_local:
            value = self.local_cache.get(key)
            if value is None:
                return "", 404
            return value, 200
        else:
            return self.node_client.forward_get(primary.url, key)
        
    def handle_replication(self, key: str, value: str):
        if self.local_cache.put(key, value) == False:
            return "", 500
        return "", 201
    
    def handle_get_full_cache(self):
        return self.local_cache.get_full_cache(), 200