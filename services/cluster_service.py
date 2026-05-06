from models.node import NodeData
from typing import List
import time

class ClusterService:
    def __init__(self, node_map: dict[str, NodeData], suspect_threshold: int, dead_threshold: int, suspect_recovery_threshold: int, dead_recovery_threshold: int, max_backoff_interval: int):
        self.node_map = node_map
        self.suspect_threshold = suspect_threshold
        self.dead_threshold = dead_threshold
        self.suspect_recovery_threshold = suspect_recovery_threshold
        self.dead_recovery_threshold = dead_recovery_threshold
        self.max_backoff_interval = max_backoff_interval


    def get_active_nodes(self) -> List[tuple[str, str]]:
        return [
            (node_id, node_data.url)
            for node_id, node_data in self.node_map.items()
            if not node_data.is_local and (node_data.status == "alive" or node_data.status == "suspect")
        ]
    
    def update_last_ping(self, node_id: str) -> None:
        self.node_map[node_id].last_ping = time.time()

    def is_alive(self, node_id: str) -> bool:
        return self.node_map[node_id].status == "alive"
    
    def is_suspect(self, node_id: str) -> bool:
        return self.node_map[node_id].status == "suspect"

    def update_missed_pings(self, node_id: str) -> None:
        state = self.node_map[node_id]

        state.consecutive_successful_pings = 0
        state.missed_pings = min(state.missed_pings+1, self.dead_threshold)
        print(f'missed pings - {state.missed_pings} (Node {node_id})' )

        if state.missed_pings >= self.dead_threshold:
            state.status = "dead"
        elif state.missed_pings >= self.suspect_threshold:
            state.status = "suspect"
    
    def update_successful_pings(self, node_id: str) -> None:
        state = self.node_map[node_id]
        if state.status == "alive":
            return

        state.consecutive_successful_pings += 1
        print(f'consecutive successful pings - {state.consecutive_successful_pings} (Node {node_id})' )

        if state.status == "suspect":
            if state.consecutive_successful_pings >= self.suspect_recovery_threshold:
                self.mark_alive(node_id)
            else:
                state.backoff_interval /= 2
        
        elif state.status == "dead":
            if state.consecutive_successful_pings >= self.dead_recovery_threshold:
                self.mark_alive(node_id)
            else:
                state.backoff_interval /= 2

    # Should this function call node client for the temp primary node to send keys to rebalance?
    # Issue would be duplicate requests from different nodes
    def mark_alive(self, node_id: str) -> None:
        state = self.node_map[node_id]
        state.status = "alive"
        state.missed_pings = 0
        state.consecutive_successful_pings = 0
        state.backoff_interval = 1

    def should_ping(self, node_id: str) -> bool:
        state = self.node_map[node_id]

        if state.status == "dead":
            if self.time_since_last_ping(node_id) < state.backoff_interval:
                return False
            else:
                state.backoff_interval = min(state.backoff_interval * 2, self.max_backoff_interval)

        return True

    def time_since_last_ping(self, node_id: str) -> float:
        state = self.node_map[node_id]
        return time.time() - state.last_ping