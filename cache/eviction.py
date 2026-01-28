class ListNode:
    def __init__(self, key=0):
        self.key = key
        self.prev = None
        self.next = None

class LRU:
    def __init__(self):
        self.hashmap = {}

        self.head = ListNode(0)
        self.tail = ListNode(0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def on_put(self, key: str, isFull: bool) -> ListNode | None:
        evicted_node = None
        if key not in self.hashmap and isFull:
            evicted_node = self._get_lru()
            self._remove_node(evicted_node)
        elif key in self.hashmap:
            self._remove_node(self.hashmap[key])
        new_node = ListNode(key)
        self.hashmap[key] = new_node
        self._add_node(new_node)
        return evicted_node
    
    def on_get(self, key: str):
        node = self.hashmap[key]
        self._remove_node(node)
        self._add_node(node)
    
    def on_delete(self, key: str):
        node = self.hashmap[key]
        self._remove_node(node)
        del self.hashmap[key]

    def _get_lru(self) -> ListNode:
        return self.tail.prev

    def _add_node(self, node: ListNode):
        temp = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = temp
        temp.prev = node
            
    def _remove_node(self, node: ListNode):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node


class LFU:
    pass