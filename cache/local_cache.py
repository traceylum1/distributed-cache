class LocalCache:
    def __init__(self, capacity):
        self.cache = {}
        self.capacity = capacity

    def put(self, key: str, val: str):
        if len(self.cache) == self.capacity:
            print("Cache at max capacity")
            return False
        if key in self.cache:
            self.cache[key] = val
            print("Record updated")
        else:
            self.cache[key] = val
            print("Record added --", key, ":", val)
        return True

    def get(self, key: str):
        if key in self.cache:
            value = self.cache[key]
            print("Cache hit --", value)
            return value
        else:
            print("Cache miss")
            return None

    