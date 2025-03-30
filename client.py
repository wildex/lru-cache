import socket
from argparse import ArgumentParser
from typing import Optional

HOST = '127.0.0.1'

def send_command(s, command: str):
    s.sendall(command.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    print(f"Received: {data}")

def run(port: int, command: Optional[str] = None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, port))
        print(f"Connected to LRU Cache server at {HOST}:{port}")

        if command:
            send_command(s, command)
            return

        while True:
            command = input("Enter command (PUT key value [ttl] / GET key / CLN / EXIT): ")
            if command.lower() == 'exit':
                break

            send_command(s, command)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('port', type=int)
    parser.add_argument('-c', '--command', type=str, default=None)

    args = parser.parse_args()

    run(args.port, args.command)