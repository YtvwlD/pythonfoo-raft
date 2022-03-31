import pytest
from raft.server.state_machine import StateMachine

@pytest.fixture
def state_machine():
    return StateMachine()


def test_set_get_del(state_machine):
    with pytest.raises(KeyError):
        state_machine.handle(("get", "foo"))
    state_machine.handle(("set", "foo", 42))
    assert state_machine.handle(("get", "foo")) == 42
    state_machine.handle(("del", "foo"))
    with pytest.raises(KeyError):
        state_machine.handle(("get", "foo"))


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


def test_invalid(state_machine):
    with pytest.raises(NotImplementedError):
        state_machine.handle("invalid")


def test_not_found(state_machine):
    with pytest.raises(KeyError):
        state_machine.handle(("get", "nonexisting"))
    with pytest.raises(KeyError):
        state_machine.handle(("del", "nonexisting"))
