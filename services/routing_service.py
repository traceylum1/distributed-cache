import hashlib
from models.node import Node
from typing import List
import bisect

def _hash(key: str): 
    return int(hashlib.md5(key.encode()).hexdigest(), 16)


_ring = []          # sorted list of hash positions
_node_map = {}      # hash -> Node

def init_ring(nodes: List[Node]):
    """
    Initialize the consistent hash ring.
    Must be called once at startup.
    """
    global _ring, _node_map

    _ring = []
    _node_map = {}

    for node in nodes:
        h = _hash(node.id)
        _ring.append(h)
        _node_map[h] = node

    _ring.sort()

def get_primary_node(key: str) -> Node:
    if not _ring:
        raise RuntimeError("Hash ring not initialized")

    key_hash = _hash(key)

    idx = bisect.bisect_left(_ring, key_hash)

    if idx == len(_ring):
        idx = 0  # wrap around ring

    return _node_map[_ring[idx]]




# Values should contain stable and unique cache node metadata, ie {"host": "10.0.1.12", "port": 6379}
# nodes = {
#     "A": Cache(),
#     "B": Cache(),
#     "C": Cache(),
# }

# ring = {
#     hash_key(f'{node}_{i}'): f'{node}_{i}' 
#     for i in range(1, 4)
#     for node in nodes.keys()
# }

# def get_primary_node(key):
#     h = hash_key(key)
#     sorted_hashes = sorted(ring.keys())
#     for node_hash in sorted_hashes:
#         if h < node_hash:
#             return ring[node_hash].split('_')[0]
#     return ring[sorted_hashes[0]].split('_')[0]  # wrap around

# def get():
#     hash_value = _hash("user:123")
#     node_id = get_primary_node("user:123")
#     cache = nodes[node_id]
#     cache.get(hash_value)

# def set():
#     hash_value = _hash("user:123")
#     node_id = get_primary_node("user:123")
#     cache = nodes[node_id]
#     cache.set(hash_value, "marcus")