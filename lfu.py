class LFUCache:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._data = {}

    def put(self, key: int, value: str) -> None:
        if key not in self._data and len(self._data) == self._capacity:
            key2delete = next(iter(self._data))
            min_usage = self._data[key2delete]['u']

            for k in self._data:
                if self._data[k]['u'] < min_usage:
                    key2delete = k
                    min_usage = self._data[k]['u']

            del self._data[key2delete]


        self._data[key] = {'v': value, 'u': 1}

    def get(self, key: int) -> str | int:
        if key not in self._data:
            return -1

        self._data[key]['u'] += 1

        return self._data[key]['v']

    def size(self):
        return len(self._data)