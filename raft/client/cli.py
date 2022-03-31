#!/usr/bin/env python3
from ast import literal_eval
from cmd import Cmd
import json
import socket
import sys
from typing import List, Tuple

HOST = '::1'
PORT = 1234
SIZE = 1024


class CliClient(Cmd):
    prompt: str = "(raft) "
    client: socket.socket

    def __init__(self, host: str, port: int):
        self.client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.client.connect((host, port))
        super().__init__()
    
    def do_get(self, key: str):
        """Get a value for a key."""
        self.query("get", key)
    
    def do_set(self, key: str, value: str):
        """Set a key's value."""
        try:
            value = literal_eval(value)
        except:
            pass
        self.query("set", key, value)
    
    def do_del(self, key: str):
        """Delete a key."""
        self.query("del", key)
    
    def do_EOF(self):
        self.do_exit()
    
    def do_exit(self):
        """Close the connection."""
        self.client.close()
        sys.exit()
    
    def onecmd(self, line: str):
        line = line.strip()
        command, *args = line.split(" ", 2)
        if command == "help" and not args:
            args = ("",)
        func = getattr(self, 'do_' + command)
        func(*args)
    
    def query(self, command: str, *args: str):
        self.client.send(json.dumps((
            command, *args,
        )).encode())
        response = json.loads(self.client.recv(SIZE).decode())
        if response["status"] == "ok":
            print("OK:", response["result"])
        elif response["status"] == "err":
            print("ERR:", response["reason"])
        else:
            raise NotImplementedError(response["status"])



if __name__ == "__main__":
    CliClient(HOST, PORT).cmdloop()
