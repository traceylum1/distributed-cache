class LocalCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, hash_key):
        if hash_key in self.cache:
            print("Cache hit --", self.cache[hash_key])
        else:
            print("Cache miss")

    def set(self, hash_key, val):
        if hash_key in self.cache:
            print("Error: Cache key collision")
            return
        self.cache[hash_key] = val
        print("New record added --", hash_key, ":", val)
