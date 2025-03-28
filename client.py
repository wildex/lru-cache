import socket
from argparse import ArgumentParser

HOST = '127.0.0.1'

def run(port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port))
        print(f"Connected to LRU Cache server at {HOST}:{port}")

        while True:
            command = input("Enter command (PUT key value / GET key / EXIT): ")
            if command.lower() == 'exit':
                break

            s.sendall(command.encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
            print(f"Received: {data}")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('port', type=int)

    args = parser.parse_args()

    run(args.port)