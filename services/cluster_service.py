from ..models.node import NodeState, Node
from typing import List
import time


class ClusterService:
    def __init__(self, nodes: List[Node], failure_threshold: int):
        self.cluster_map: dict[str, NodeState] = {}
        self.failure_threshold = failure_threshold

        for node in nodes:
            self.cluster_map[node.id] = NodeState(status="alive", missed_pings="0")

    def get_active_nodes(self) -> List[str]:
        active_nodes = []
        for node_id, node_state in self.cluster_map.items():
            if node_state.status == "alive":
                active_nodes.append(node_id)
        return active_nodes

    def is_alive(self, node_id: str) -> bool:
        return self.cluster_map[node_id].status == "alive"

    def update_missed_pings(self, node_id: str) -> None:
        self.cluster_map[node_id].missed_pings += 1
        if self.cluster_map[node_id].missed_pings == 1:
            self.mark_suspect(node_id)
        elif self.cluster_map[node_id].missed_pings == self.failure_threshold:
            self.mark_dead(node_id)
    
    def mark_suspect(self, node_id: str) -> None:
        if self.cluster_map[node_id].status == "alive":
            self.cluster_map[node_id].status = "suspect"
    
    def mark_dead(self, node_id: str) -> None:
        if self.cluster_map[node_id].status == "suspect":
            self.cluster_map[node_id].status = "dead"

    def mark_alive(self, node_id: str) -> None:
        if self.cluster_map[node_id].status == "dead":
            self.cluster_map[node_id].status = "alive"

    
