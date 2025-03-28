import threading
from argparse import ArgumentParser
from lru import LRUCache

import socket

HOST = '127.0.0.1'

def handle_client(conn, addr, cache):
    with conn:
        print(f"Connected by {addr}")
        try:
            while True:
                data = conn.recv(1024).decode('utf-8').strip()
                if not data:
                    break

                try:
                    command, key, *value = data.split()
                    key = int(key)

                    if command.lower() == 'put':
                        value = value[0] if value else ""
                        cache.put(key, value)
                        response = f"Put: {key} -> {value}"
                    elif command.lower() == 'get':
                        result = cache.get(key)
                        response = f"Get: {key} -> {result}"
                    else:
                        response = f"Unknown command: {command}"
                except ValueError:
                    response = "Invalid input format. Use 'PUT key value' or 'GET key'"

                conn.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
        finally:
            print(f"Closing connection from {addr}")
            conn.close()

def run(port: int, cache_size: int):
    cache = LRUCache(cache_size)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port))
        s.listen()

        print(f"LRU Cache is running. Cache size: {cache_size}  Listening on {HOST}:{port}")

        try:
            while True:
                conn, addr = s.accept()

                t = threading.Thread(target=handle_client, args=(conn, addr, cache))
                t.start()
        except KeyboardInterrupt:
            print("Server is shutting down.")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('port', type=int)
    parser.add_argument('size', type=int)

    args = parser.parse_args()

    run(port=args.port, cache_size=args.size)


