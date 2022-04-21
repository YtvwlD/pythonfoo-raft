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
    server.handle_command_from_client(client, b'["set", "foo", 5]')
    client.send.assert_called_once_with(b'{"status": "ok", "result": null}')


def test_set_value_str(server, client):
    server.handle_command_from_client(client, b"set foo 5")
    client.send.assert_called_once_with(b'{"status": "ok", "result": null}')


def test_get_nonexisting(server, client):
    server.handle_command_from_client(client, b"get bar")
    client.send.assert_called_once_with(b'{"status": "err", "reason": "KeyError"}')