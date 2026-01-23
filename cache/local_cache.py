class LocalCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str):
        if key in self.cache:
            print("Cache hit --", self.cache[key])
        else:
            print("Cache miss")

    def put(self, key: str, val: str):
        if key in self.cache:
            print("Error: Cache key collision")
            return
        self.cache[key] = val
        print("New record added --", key, ":", val)
