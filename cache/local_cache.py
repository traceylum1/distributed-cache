from .eviction import LRU, LFU
from .expiration import TTL

class LocalCache:
    def __init__(self, capacity: int, eviction: LRU | LFU, expiration: TTL):
        self.cache = {}
        self.capacity = capacity
        self.eviction = eviction
        self.expiration  = expiration

    def put(self, key: str, val: str):
        self.expiration.on_put(key)
        evicted = self.eviction.on_put(key, len(self.cache) == self.capacity)
        if evicted:
            print("Evicted key --", evicted.key)
            self._delete(evicted.key)
        self.cache[key] = val
        print("Cache put successful --", key, ":", val)
        return True

    def get(self, key: str):
        if key in self.cache:
            if self.expiration.is_expired(key):
                self._delete(key)
                print("Key is expired")
                return None
            else:
                self.eviction.on_get(key)
                value = self.cache[key]
                print("Cache hit --", value)
                return value
        else:
            print("Cache miss")
            return None

    def _delete(self, key: str):
        self.eviction.on_delete(key)
        self.expiration.on_delete(key)
        del self.cache[key]