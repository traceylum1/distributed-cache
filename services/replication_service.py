from typing import List
from models.node import Node

def replicate_to(self, replicas: List[Node], key: str, value: str):
    print("calling node_client replicate_to")
    futures = []
    for r in replicas:
        futures.append(self.send_put_async(r, key, value))
    wait_for_all(futures)