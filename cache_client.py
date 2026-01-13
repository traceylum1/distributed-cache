import hashlib
from cache.cache import Cache

def hash_key(key): 
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

# Values should contain stable and unique cache node metadata, ie {"host": "10.0.1.12", "port": 6379}
nodes = {
    "A": Cache(),
    "B": Cache(),
    "C": Cache(),
}

ring = {
    hash_key(f'{node}_{i}'): f'{node}_{i}' 
    for i in range(1, 4)
    for node in nodes.keys()
}

def get_node(key):
    h = hash_key(key)
    sorted_hashes = sorted(ring.keys())
    for node_hash in sorted_hashes:
        if h < node_hash:
            return ring[node_hash].split('_')[0]
    return ring[sorted_hashes[0]].split('_')[0]  # wrap around

def get():
    hash_value = hash_key("user:123")
    node_id = get_node("user:123")
    cache = nodes[node_id]
    cache.get(hash_value)

def set():
    hash_value = hash_key("user:123")
    node_id = get_node("user:123")
    cache = nodes[node_id]
    cache.set(hash_value, "marcus")