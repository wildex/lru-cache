import time

from lfu import LFUCache
from lru import LRUCache

if __name__ == "__main__":
    ###
    ### Test LFU
    ###

    cache = LFUCache(3)

    cache.put(1, 'A')
    cache.get(1)
    cache.get(1)

    cache.put(2, 'B')
    cache.get(2)
    cache.get(2)

    cache.put(3, 'C')
    cache.get(3)

    cache.put(4, 'D')
    cache.put(3, 'C')

    assert cache.size() == 3
    assert cache.get(1) == 'A'
    assert cache.get(5) == -1
    assert cache.get(4) == -1
    assert cache.get(3) == 'C'

    ###
    ### Test LRU
    ###

    print("### Test LRU Cache ###")
    print("Create LRU Cache size 3")
    cache = LRUCache(3)

    print("Insert 1 A")
    cache.put(1, 'A')
    print("Insert 2 B")
    cache.put(2, 'B')
    print("Insert 3 C")
    cache.put(3, 'C')

    print("Insert 4 D")
    cache.put(4, 'D')

    print("Assert 1 does not exists")
    assert cache.get(1) == -1

    print("Assert 4 exists and has proper value")
    assert cache.get(4) == 'D'

    print("Insert 5 K")
    cache.put(5, 'K')

    print("Assert 5 exists and has proper value")
    assert cache.get(5) == 'K'

    print("Assert 2 does not exists")
    assert cache.get(2) == -1

    print("Assert 6 does not exists")
    assert cache.get(6) == -1

    print("Override 5 G")
    cache.put(5, 'G')

    print("Assert 5 exists and has proper value")
    assert cache.get(5) == 'G'

    print("Test overwrite keys")
    cache = LRUCache(2)
    cache.put(1, 'A')
    cache.put(1, 'B')
    cache.put(2, 'C')

    assert cache.get(1) == 'B'
    assert cache.get(2) == 'C'

    print("Test LruCache expiration")
    cache = LRUCache(2)

    cache.put(1, 'A')
    cache.put(2, 'B', 1)

    time.sleep(2)

    cache.cleanup()

    assert cache.get(1) == 'A'
    assert cache.get(2) == -1

    cache.put(2, 'B')
    assert cache.get(2) == 'B'




