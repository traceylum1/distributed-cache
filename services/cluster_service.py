from models.node import NodeData
from typing import List
import time

class ClusterService:
    def __init__(self, node_map: dict[str, NodeData], suspect_threshold: int, failure_threshold: int):
        self.node_map = node_map
        self.suspect_threshold = suspect_threshold
        self.failure_threshold = failure_threshold


    def get_active_nodes(self) -> List[tuple[str, str]]:
        return [
            (node_id, node_data.url)
            for node_id, node_data in self.node_map.items()
            if not node_data.is_local and (node_data.status == "alive" or node_data.status == "suspect")
        ]

    def is_alive(self, node_id: str) -> bool:
        return self.node_map[node_id].status == "alive"
    
    def is_suspect(self, node_id: str) -> bool:
        return self.node_map[node_id].status == "suspect"

    def update_missed_pings(self, node_id: str) -> None:
        state = self.node_map[node_id]
        state.missed_pings = min(state.missed_pings+1, self.failure_threshold)
        print(f'missed pings - {state.missed_pings} (Node {node_id})' )

        if state.missed_pings >= self.failure_threshold:
            state.status = "dead"
        elif state.missed_pings >= self.suspect_threshold:
            state.status = "suspect"

    def mark_alive(self, node_id: str) -> None:
        state = self.node_map[node_id]
        state.status = "alive"
        state.missed_pings = 0
        state.backoff_interval = 0

    def should_ping(self, node_id: str) -> bool:
        state = self.node_map[node_id]

        if state.status == "dead":
            state.backoff_interval *= 2
            return self.time_since_last_ping(node_id) > state.backoff_interval

        return True

    def time_since_last_ping(self, node_id: str) -> float:
        state = self.node_map[node_id]
        return time.time() - state.last_ping