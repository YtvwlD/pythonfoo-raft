import pytest
from raft.server.state_machine import StateMachine

@pytest.fixture
def state_machine():
    return StateMachine()


@pytest.mark.parametrize("key", ["foo", "foo bar", "fööbär", "", "😊"])
@pytest.mark.parametrize("value", [42, "abcdef", None, True, 1.2])
def test_set_get_del(state_machine, key, value):
    with pytest.raises(KeyError):
        state_machine.handle(("get", key))
    state_machine.handle(("set", key, value))
    assert state_machine.handle(("get", key)) == value
    state_machine.handle(("del", key))
    with pytest.raises(KeyError):
        state_machine.handle(("get", key))


def test_set_change(state_machine):
    state_machine.handle(("set", "foo", 42))
    assert state_machine.handle(("get", "foo")) == 42
    state_machine.handle(("set", "foo", 23))
    assert state_machine.handle(("get", "foo")) == 23


def test_set_multiple(state_machine):
    state_machine.handle(("set", "foo", 42))
    state_machine.handle(("set", "bar", 23))
    assert state_machine.handle(("get", "foo")) == 42
    assert state_machine.handle(("get", "bar")) == 23


def test_invalid_command(state_machine):
    with pytest.raises(NotImplementedError):
        state_machine.handle("invalid")


def test_invalid(state_machine):
    with pytest.raises(TypeError):
        state_machine.handle(("get", 0))
    with pytest.raises(TypeError):
        state_machine.handle(("set", 0, 5))
    with pytest.raises(TypeError):
        state_machine.handle(("del", 0))




@pytest.mark.parametrize("command", ["get", "del"])
def test_not_found(state_machine, command):
    with pytest.raises(KeyError):
        state_machine.handle((command, "nonexisting"))
