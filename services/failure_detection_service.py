import threading
import time

"""
Failure detection will use pinging (pull-based) and gossip
- If a ping fails, spread suspicion to other nodes via gossip
- Other nodes ping suspect node
"""
class FailureDetection:
    def __init__(self, cluster_service, interval=3):
        self.cluster_service = cluster_service
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
            self.node_client.send_ping()
            time.sleep(self.interval)