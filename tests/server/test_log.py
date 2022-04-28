import pytest
from raft.server.log import Entry, Log


@pytest.fixture
def log():
    return Log()


def test_heartbeat(log):
    term, res = log.append_entries(0, 0, -1, 0, [], -1)
    assert term == 0
    assert res == True
    assert log.entries == []
    assert log.commit_index == -1


def test_first_log_entry(log):
    term, res = log.append_entries(0, 0, -1, 0, [Entry(0, ("set", "foo", 5))], -1)
    assert term == 0
    assert res == True
    assert log.entries == [Entry(0, ("set", "foo", 5))]
    assert log.commit_index == -1


def test_log_append(log):
    term, res = log.append_entries(0, 0, -1, 0, [Entry(0, ("set", "foo", 5))], -1)
    assert term == 0
    assert res == True
    term, res = log.append_entries(
        term, 0, 0, term, [Entry(0, ("set", "bar", 42))], -1
    )
    assert term == 0
    assert res == True
    assert log.entries == [
        Entry(0, ("set", "foo", 5)), Entry(0, ("set", "bar", 42))
    ]
    assert log.commit_index == -1


def test_log_append_commit(log):
    term, res = log.append_entries(
        0, 0, -1, 0, [Entry(0, ("set", "foo", 5))], 0
    )
    assert term == 0
    assert res == True
    term, res = log.append_entries(
        term, 0, 0, term, [Entry(0, ("set", "bar", 42))], 1
    )
    assert term == 0
    assert res == True
    assert log.entries == [
        Entry(0, ("set", "foo", 5)), Entry(0, ("set", "bar", 42))
    ]
    assert log.commit_index == 1


def test_log_append_commit_delay(log):
    term, res = log.append_entries(
        0, 0, -1, 0, [Entry(0, ("set", "foo", 5))], -1
    )
    assert term == 0
    assert res == True
    term, res = log.append_entries(
        term, 0, 0, term, [Entry(0, ("set", "bar", 42))], 0
    )
    assert term == 0
    assert res == True
    assert log.entries == [
        Entry(0, ("set", "foo", 5)), Entry(0, ("set", "bar", 42))
    ]
    assert log.commit_index == 0


def test_ignores_old_entries(log):
    term, res = log.append_entries(2, 0, -1, 0, [Entry(2, ("set", "foo", 5))], -1)
    assert term == 2
    assert res == True
    term, res = log.append_entries(1, 0, 0, 0, [Entry(1, ("set", "foo", 2))], -1)
    assert term == 2
    assert res == False
    assert log.entries == [Entry(2, ("set", "foo", 5))]
    assert log.commit_index == -1


def test_ignores_conflicting_entries(log):
    term, res = log.append_entries(2, 0, -1, 0, [Entry(2, ("set", "foo", 5))], -1)
    assert term == 2
    assert res == True
    term, res = log.append_entries(2, 0, 0, 1, [Entry(2, ("set", "foo", 2))], -1)
    assert term == 2
    assert res == False
    assert log.entries == [Entry(2, ("set", "foo", 5))]
    assert log.commit_index == -1


def test_missing_entries(log):
    # initial entry
    term, res = log.append_entries(
        2, 0, -1, 0, [Entry(2, ("set", "foo", 5))], -1)
    assert term == 2
    assert res == True
    # write another entry
    term, res = log.append_entries(
        2, 0, 0, 2, [Entry(2, ("set", "foo", 2))], -1)
    assert term == 2
    assert res == True
    # another one, but one missing in between
    term, res = log.append_entries(
        2, 0, 2, 2, [Entry(2, ("set", "bar", 23))], -1
    )
    assert term == 2
    assert res == False
    assert log.entries == [
        Entry(2, ("set", "foo", 5)), Entry(2, ("set", "foo", 2))
    ]
    assert log.commit_index == -1


def test_overwrites_conflicting_entries(log):
    # initial entry
    term, res = log.append_entries(2, 0, -1, 0, [Entry(2, ("set", "foo", 5))], -1)
    assert term == 2
    assert res == True
    # write another entry
    term, res = log.append_entries(2, 0, 0, 2, [Entry(2, ("set", "foo", 2))], -1)
    assert term == 2
    assert res == True
    # another one
    term, res = log.append_entries(
        2, 0, 1, 2, [Entry(2, ("set", "bar", 23))], -1
    )
    assert term == 2
    assert res == True
    # oops, that was wrong
    term, res = log.append_entries(
        3, 1, 1, 3, [Entry(3, ("set", "bar", 42))], -1
    )
    assert term == 3
    assert res == False
    # re-sync
    term, res = log.append_entries(
        3, 1, 0, 2, [
            Entry(2, ("set", "foo", 2)), Entry(3, ("set", "bar", 42))
        ], -1
    )
    assert term == 3
    assert res == True
    assert log.entries == [
        Entry(2, ("set", "foo", 5)),
        Entry(2, ("set", "foo", 2)),
        Entry(3, ("set", "bar", 42)),
    ]
    assert log.commit_index == -1


def test_overwrites_conflicting_entries_early(log):
    # this probaly doesn't happen, but well

    # initial entry
    term, res = log.append_entries(
        2, 0, -1, 0, [Entry(2, ("set", "foo", 5))], -1)
    assert term == 2
    assert res == True
    # write another entry
    term, res = log.append_entries(
        2, 0, 0, 2, [Entry(2, ("set", "foo", 2))], -1)
    assert term == 2
    assert res == True
    # another one
    term, res = log.append_entries(
        2, 0, 1, 2, [Entry(2, ("set", "bar", 23))], -1
    )
    assert term == 2
    assert res == True
    # new leader
    term, res = log.append_entries(
        3, 1, 1, 3, [Entry(3, ("set", "bar", 42))], -1
    )
    assert term == 3
    assert res == False
    # early re-sync
    term, res = log.append_entries(
        3, 1, -1, 2, [
            Entry(2, ("set", "foo", 5)),
            Entry(2, ("set", "foo", 2)), 
            Entry(3, ("set", "bar", 42)),
        ], -1
    )
    assert term == 3
    assert res == True
    assert log.entries == [
        Entry(2, ("set", "foo", 5)),
        Entry(2, ("set", "foo", 2)),
        Entry(3, ("set", "bar", 42)),
    ]
    assert log.commit_index == -1
