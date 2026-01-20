from cache import local_cache
from services.routing_service import get_primary_node
from clients.node_client import send_put

def handle_put(key, value):
    node = get_primary_node(key)

    if node.is_local:
        local_cache.set(key, value)
    else:
        send_put(node.url, key, value)
        