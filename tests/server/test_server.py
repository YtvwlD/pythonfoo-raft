import pytest
from unittest.mock import MagicMock, patch
from raft.server.server import Server


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
