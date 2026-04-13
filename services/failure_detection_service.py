import threading
import time
from models.node import NodeData
from clients.node_client import NodeClient
from services.cluster_service import ClusterService

"""
Failure detection will use pinging (pull-based)
- If a ping fails, mark as suspect
- If it fails n times, mark as dead
- Eventually consistent with slow convergence

With gossip:
- If a ping fails, spread suspicion to other nodes via gossip
- Other nodes ping suspect node, if majority marks suspect, mark dead
- Eventually consistent with faster convergence

TODO:
- Figure out if threading.Event() is needed in this circumstance
"""
class FailureDetection:
    def __init__(self, node_map: dict[str, NodeData], cluster_service: ClusterService, node_client: NodeClient, interval=3):
        self.node_map = node_map
        self.cluster_service = cluster_service
        self.node_client = node_client
        self.interval = interval
        self._stop_event = threading.Event()

    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            # Example: failure detection
            for node_id, node_data in self.node_map.items():
                if not node_data.is_local and self.cluster_service.should_ping(node_id):
                    self.cluster_service.update_last_ping(node_id)
                    self.node_client.send_ping(node_id, node_data.url)
            time.sleep(self.interval)