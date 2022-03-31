#!/usr/bin/env python3
import json
from threading import Thread
import traceback
from typing import List
import socket
from state_machine import StateMachine

SIZE = 1024
HOST = '::1'
PORT = 1234
BACKLOG = 5


class Server:
    machine: StateMachine
    sock: socket.socket
    threads: List[Thread]

    def __init__(self, host: str, port: int):
        self.machine = StateMachine()
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(BACKLOG)
        self.threads = list()
    
    def run(self):
        while True:
            client, address = self.sock.accept()
            thread = Thread(target=self.handle_client, args=(client,))
            thread.start()
            self.threads.append(thread)

    def handle_client(self, client: socket.socket):
        with client:
            while (data := client.recv(SIZE)):
                try:
                    command = json.loads(data.decode())
                except:
                    # try to parse as a string
                    command = data.decode().strip().split(" ", 2)
                print(">", command)
                try:
                    result = {
                        "status": "ok",
                        "result": self.machine.handle(command),
                    }
                except Exception as exc:
                    traceback.print_exc()
                    result = {
                        "status": "err",
                        "reason": type(exc).__name__,
                    }
                print("<", result)
                client.send(json.dumps(result).encode())


if __name__ == "__main__":
    server = Server(HOST, PORT)
    server.run()
