import time

class TTL:
    def __init__(self, ttl=10):
        self.hashmap = {}
        self.ttl = ttl  # seconds
    
    def on_put(self, key: str, write_timestamp: float):
        self.hashmap[key] = write_timestamp + self.ttl
    
    def is_expired(self, key: str) -> bool:
        return self.hashmap[key] < time.time()
    
    def on_delete(self, key: str):
        del self.hashmap[key]