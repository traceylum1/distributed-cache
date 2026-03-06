import threading
import time
from ..clients.node_client import NodeClient
from .cluster_service import ClusterService

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
    def __init__(self, cluster_service: ClusterService, node_client: NodeClient, interval=3):
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
            active_nodes = self.cluster_service.get_active_nodes()
            for n_id in active_nodes:
                self.node_client.send_ping(n_id)
            time.sleep(self.interval)