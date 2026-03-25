from models.node import NodeState, Node
from typing import List

class ClusterService:
    def __init__(self, nodes: List[Node], suspect_threshold: int, failure_threshold: int):
        self.cluster_map: dict[str, NodeState] = {}
        self.suspect_threshold = suspect_threshold
        self.failure_threshold = failure_threshold

        for node in nodes:
            self.cluster_map[node.id] = NodeState(status="alive", missed_pings=0)

    def get_active_nodes(self) -> List[str]:
        return [
            node_id
            for node_id, state in self.cluster_map.items()
            if state.status == "alive" or state.status == "suspect"
        ]

    def is_alive(self, node_id: str) -> bool:
        return self.cluster_map[node_id].status == "alive"
    
    def is_suspect(self, node_id: str) -> bool:
        return self.cluster_map[node_id].status == "suspect"

    def update_missed_pings(self, node_id: str) -> None:
        state = self.cluster_map[node_id]
        state.missed_pings += 1

        if state.missed_pings >= self.failure_threshold:
            state.status = "dead"
        elif state.missed_pings >= self.suspect_threshold:
            state.status = "suspect"

    def mark_alive(self, node_id: str) -> None:
        state = self.cluster_map[node_id]
        state.status = "alive"
        state.missed_pings = 0

    
