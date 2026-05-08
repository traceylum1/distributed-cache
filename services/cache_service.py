from services.routing_service import RoutingService
from clients.node_client import NodeClient
from cache.local_cache import LocalCache
from services.replication_service import replicate_to
import time

class CacheService:
    def __init__(self, routing_service: RoutingService, node_client: NodeClient, local_cache: LocalCache):
        self.routing_service = routing_service
        self.node_client = node_client
        self.local_cache = local_cache

    async def handle_put(self, key: str, value: str):
        nodes, _ = self.routing_service.get_primary_and_replica_nodes(key)

        primary = nodes[0]
        replicas = nodes[1:]
        print(primary)

        write_timestamp = time.time()

        if primary.is_local:
            if self.local_cache.put(key, value, write_timestamp) == False:
                return "", 500
            await replicate_to(self.node_client, replicas, key, value, write_timestamp)
            return "", 200

        else:
            return self.node_client.forward_put(primary.url, key, value)


    """
    handle_get:
        - if local node has key, return value
        - else, forward requests to primary, then replicas if necessary
            - loop until the first successful read request
    """
    def handle_get(self, key: str):
        nodes, local_has_key = self.routing_service.get_primary_and_replica_nodes(key)

        if local_has_key:
            value = self.local_cache.get(key)
            return value, 200

        for node in nodes:
            value, status_code = self.node_client.forward_get(node.url, key)
            if status_code == 200:
                return value, 200
            
        return "", 500
        
    def handle_replication(self, key: str, value: str, write_timestamp: float):
        if self.local_cache.put(key, value, write_timestamp) == False:
            return "", 500
        return "", 201
    
    def handle_get_full_cache(self):
        return self.local_cache.get_full_cache(), 200