from types import TracebackType
import pytest
from typing import List
from unittest.mock import MagicMock, patch
from raft.server.server import Server

class FakeClient:
    commands: List[bytes]
    responses: List[bytes]

    def __init__(self, commands: List[bytes]):
        self.commands = commands
        self.responses = []
    
    def __enter__(self):
        pass
    
    def __exit__(
        self, exc_type: type, exc_value: Exception, traceback: TracebackType
    ):
        pass
    
    def recv(self, size: int) -> bytes:
        if self.commands:
            return self.commands.pop(0)
        else:
            return b""
    
    def send(self, message: bytes) -> int:
        self.responses.append(message)
        return len(message)

@pytest.fixture
def client():
    return MagicMock()


@pytest.fixture
def server():
    patch("socket.socket")
    return Server("localhost", 1234)


def test_set_value_json(server, client):
    resp = server.handle_command_from_client(client, b'["set", "foo", 5]')
    assert resp == b'{"status": "ok", "result": null}'


def test_set_value_str(server, client):
    resp = server.handle_command_from_client(client, b"set foo 5")
    assert resp == b'{"status": "ok", "result": null}'


def test_get_nonexisting(server, client):
    resp = server.handle_command_from_client(client, b"get bar")
    assert resp == b'{"status": "err", "reason": "KeyError"}'


def test_handle_client(server):
    client = FakeClient([b"set foo 5"])
    server.handle_client(client)
    assert client.responses == [b'{"status": "ok", "result": null}']
