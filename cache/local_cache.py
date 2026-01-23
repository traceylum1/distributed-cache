class LocalCache:
    def __init__(self):
        self.cache = {}

    def put(self, key: str, val: str):
        self.cache[key] = val
        print("New record added --", key, ":", val)

    def get(self, key: str):
        if key in self.cache:
            value = self.cache[key]
            print("Cache hit --", value)
            return value
        else:
            print("Cache miss")
            return None

    