import hashlib
from models.node import Node
from typing import List
import bisect

class RoutingService:
    def __init__(self, nodes: List[Node]):
        self.ring = []
        self.node_map = {}

        for node in nodes:
            h = self._hash(node.id)
            self.ring.append(h)
            self.node_map[h] = node

        self.ring.sort()
        print("ring", self.ring)
        print("node map", self.node_map)

    def _hash(self, key: str): 
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def get_primary_node(self, key: str) -> Node:
        key_hash = self._hash(key)

        idx = bisect.bisect_left(self.ring, key_hash)

        if idx == len(self.ring):
            idx = 0  # wrap around ring

        return self.node_map[self.ring[idx]]
