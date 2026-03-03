from ..models.node import NodeState, Node
from typing import List
import time


class ClusterService:
    def __init__(self, nodes: List[Node]):
        self.cluster_map = {}

        for node in nodes:
            self.cluster_map[node.id] = NodeState(status="alive", last_heartbeat="0")

    def get_active_nodes(self) -> List[str]:
        active_nodes = []
        for node_id, state in self.cluster_map:
            if state.status == "alive":
                active_nodes.append(node_id)
        return active_nodes

    def is_alive(self, node_id: str) -> bool:
        return self.cluster_map[node_id].status == "alive"
    
    def mark_suspect(self, node_id: str) -> None:
        self.cluster_map[node_id].status == "suspect"
    
    def mark_dead(self, node_id: str) -> None:
        self.cluster_map[node_id].status == "dead"

    def mark_alive(self, node_id: str) -> None:
        self.cluster_map[node_id].status == "alive"

    def update_heartbeat(self, node_id: str) -> None:
        self.cluster_map[node_id].last_heartbeat == time.time()
    
