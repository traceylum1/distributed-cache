import hashlib
from models.node import Node
from services.cluster_service import ClusterService
from typing import List
import bisect

class RoutingService:
    def __init__(self, nodes: List[Node], cluster_service: ClusterService, replication_factor: int):
        self.ring = []
        self.node_map = {}
        self.replication_factor = replication_factor
        self.cluster_service = cluster_service

        for node in nodes:
            h = self._hash(node.id)
            self.ring.append(h)
            self.node_map[h] = node

        self.ring.sort()
        print("ring", self.ring)
        print("node map", self.node_map)

    def _hash(self, key: str): 
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    """
    get_nodes_for_key: 
        - gets primary and replica nodes
        - returns them in an ordered list [primary, replica1, replica2, ...]
    """
    def get_primary_and_replica_nodes(self, key: str) -> Node:
        key_hash = self._hash(key)

        idx = bisect.bisect_left(self.ring, key_hash)
        if idx == len(self.ring):
            idx = 0  # wrap around ring
        
        nodes = []

        for i in range(self.replication_factor):
            curr_idx = (idx + i) % len(self.ring)
            nodes.append(self.node_map[self.ring[curr_idx]])

        return nodes