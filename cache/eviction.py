class ListNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRU:
    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0

        self.head = ListNode(0,0)
        self.tail = ListNode(0,0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def add(self, key, val):
        if self.size == self.capacity:

            
    

    def remove(self):
        pass