#!/usr/bin/env python3
import socket

SIZE = 1024
HOST = '::1'
PORT = 1234
BACKLOG = 5


def handle_single_client(client):
    with client:
        while (data := client.recv(SIZE)):
            print(data.decode())
            client.send(data)


def main():
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(BACKLOG)
    while True:
        client, address = s.accept()
        handle_single_client(client)


if __name__ == "__main__":
    main()
