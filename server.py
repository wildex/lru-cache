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
                    params = data.split()
                    command = params[0]

                    if command.lower() == 'put':
                        key, *additional_args = params[1:]
                        key = int(key)

                        value = additional_args[0] if additional_args else ""
                        ttl = int(additional_args[1]) if len(additional_args) > 1 else None

                        cache.put(key, value, ttl)
                        response = f"Put: {key} -> {value}"
                    elif command.lower() == 'get':
                        key = int(params[1])

                        result = cache.get(key)
                        response = f"Get: {key} -> {result}"
                    elif command.lower() == 'cln':
                        cache.cleanup()
                        response = f"Cleanup"
                    else:
                        response = f"Unknown command: {command}"
                except ValueError as e:
                    print(e)
                    response = "Invalid input format. Use 'PUT key value [ttl]' or 'GET key' or 'CLN'"

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


