import hashlib
from models.node import NodeData
from services.cluster_service import ClusterService
from typing import List
import bisect

class RoutingService:
    def __init__(self, node_map: dict[str, NodeData], cluster_service: ClusterService, replication_factor: int):
        self.ring = []
        self.node_hash = {}
        self.node_map = node_map
        self.replication_factor = replication_factor
        self.cluster_service = cluster_service

        for node_id, node_data in self.node_map.items():
            h = self._hash(node_id)
            self.ring.append(h)
            self.node_hash[h] = node_data

        self.ring.sort()
        print("ring", self.ring)
        print("node map", self.node_hash)

    def _hash(self, key: str): 
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    """
    get_nodes_for_key: 
        - gets primary and replica nodes
        - returns them in an ordered list [primary, replica1, replica2, ...]
    """
    def get_primary_and_replica_nodes(self, key: str) -> List[NodeData]:
        key_hash = self._hash(key)

        idx = bisect.bisect_left(self.ring, key_hash)
        if idx == len(self.ring):
            idx = 0  # wrap around ring
        
        nodes = []

        for i in range(self.replication_factor):
            curr_idx = (idx + i) % len(self.ring)
            nodes.append(self.node_hash[self.ring[curr_idx]])

        return nodes