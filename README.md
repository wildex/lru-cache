# LRU Cache

Double linked list + dict LRU Cache implementation with example socket server and client

Running:

- `poetry install`
- `source .venv/bin/activate`
- `python server.py 65432 200`
- `python client.py 65432`

There is also attempt to implement LFU cache, located in lfu.py

test.py includes some basic test cases using standard assertions