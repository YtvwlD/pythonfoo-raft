#!/usr/bin/env python3
import socket

host = '::1'
port = 1234
SIZE = 1024
client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
client.connect((host, port))

def main():
    with client:
        while (line := input("> ")):
            client.send(line.encode())
            data = client.recv(SIZE)
            print("<", data.decode())


if __name__ == "__main__":
    main()
