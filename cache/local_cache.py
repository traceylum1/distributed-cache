from .eviction import LRU, LFU

class LocalCache:
    def __init__(self, capacity: int, eviction: LRU | LFU):
        self.cache = {}
        self.capacity = capacity
        self.eviction = eviction

    def put(self, key: str, val: str):
        evicted = self.eviction.on_put(key, len(self.cache) == self.capacity)
        if evicted:
            print("Evicted --", evicted.key)
            del self.cache[evicted.key]
        self.cache[key] = val
        print("Cache put successful --", key, ":", val)
        return True

    def get(self, key: str):
        if key in self.cache:
            self.eviction.on_get(key)
            value = self.cache[key]
            print("Cache hit --", value)
            return value
        else:
            print("Cache miss")
            return None

    