from models.node import NodeData
from typing import List

class ClusterService:
    def __init__(self, node_map: dict[str, NodeData], suspect_threshold: int, failure_threshold: int):
        self.node_map = node_map
        self.suspect_threshold = suspect_threshold
        self.failure_threshold = failure_threshold


    def get_active_nodes(self) -> List[tuple[str, str]]:
        return [
            (node_id, node_data.url)
            for node_id, node_data in self.node_map
            if node_data.status == "alive" or node_data.status == "suspect"
        ]

    def is_alive(self, node_id: str) -> bool:
        return self.node_map[node_id].status == "alive"
    
    def is_suspect(self, node_id: str) -> bool:
        return self.node_map[node_id].status == "suspect"

    def update_missed_pings(self, node_id: str) -> None:
        state = self.node_map[node_id]
        state.missed_pings += 1

        if state.missed_pings >= self.failure_threshold:
            state.status = "dead"
        elif state.missed_pings >= self.suspect_threshold:
            state.status = "suspect"

    def mark_alive(self, node_id: str) -> None:
        state = self.node_map[node_id]
        state.status = "alive"
        state.missed_pings = 0

    
