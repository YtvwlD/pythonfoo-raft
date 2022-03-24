#!/usr/bin/env python3
from threading import Thread
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
    threads = list()
    while True:
        client, address = s.accept()
        thread = Thread(target=handle_single_client, args=(client,))
        thread.start()
        threads.append(thread)


if __name__ == "__main__":
    main()
