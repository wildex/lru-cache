import time
from typing import Self
from typing import Optional
from threading import Lock

class Node:
    def __init__(
        self,
        key: Optional[int] = None,
        value: Optional[str] = None,
        expiration: Optional[int] = None,
    ):
        self._key = key
        self._value = value
        self._expiration = expiration
        self._prev = None
        self._next = None

    @property
    def prev(self):
        return self._prev

    @property
    def next(self):
        return self._next

    @prev.setter
    def prev(self, n: Self):
        self._prev = n

    @next.setter
    def next(self, n: Self):
        self._next = n

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

    @property
    def expiration(self):
        return self._expiration

class LRUCache:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("Capacity must be at least 1")

        self._capacity = capacity
        self._curr_size = 0

        self._head = Node()
        self._tail = Node()

        self._head.prev = self._tail
        self._head.next = self._tail
        self._tail.prev = self._head
        self._tail.next = self._head

        self._data: dict[int, Node] = {}

        self._lock = Lock()

    def insert_latest(self, n: Node):
        cur_latest = self._head.next

        self._head.next = n
        cur_latest.prev = n

        n.prev = self._head
        n.next = cur_latest

    def remove_node(self, node: Node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def put(self, key: int, value: str, ttl: Optional[int] = None):
        with self._lock:
            if key in self._data:
                node = self._data[key]
                self.remove_node(node)

                self._curr_size -= 1

            if self._curr_size >= self._capacity:
                cur_oldest = self._tail.prev

                self.remove_node(cur_oldest)
                del self._data[cur_oldest.key]

                self._curr_size -= 1

            expiration = None
            if ttl:
                expiration = int(time.time()) + ttl

            new_node = Node(key, value, expiration)
            self.insert_latest(new_node)
            self._data[key] = new_node

            self._curr_size += 1

    def get(self, key: int):
        with self._lock:
            node = self._data.get(key, None)
            if not node:
                return -1

            self.remove_node(node)
            self.insert_latest(node)

            return node.value

    def cleanup(self):
        n = self._head.next
        cleanup_time = int(time.time())

        while n != self._tail:
            next_node = n.next
            if n.expiration and n.expiration <= cleanup_time:
                self.remove_node(n)
                del self._data[n.key]

            n = next_node