from typing import List, NamedTuple, Tuple

from ..utils import list_get
from .state_machine import Command

class Entry(NamedTuple):
    term: int
    command: Command


class Log:
    entries: List[Entry]
    current_term: int
    commit_index: int

    def __init__(self):
        self.entries = []
        self.current_term = 0
        self.commit_index = -1


    # TODO: is leader_id really an int?
    def append_entries(
        self, term: int, leader_id: int, prev_log_index: int,
        prev_log_term: int, entries: List[Entry], leader_commit: int
    ) -> Tuple[int, bool]:
        print("-->", entries)
        # step 1: check whether the data we received is old
        if term < self.current_term:
            return (self.current_term, False)
        if term > self.current_term:
            self.current_term = term
        # step 2: check whether we have conflicting entries
        # nb: checking the last entry is enough
        print("initial:", self.entries)
        if (prev_entry := list_get(self.entries, prev_log_index)) is not None:
            if prev_entry.term != prev_log_term:
                return (self.current_term, False)
        else:
            if self.entries and prev_log_index != -1:
                # missing entries before update
                return (self.current_term, False)
        if entries:
            # step 3: overwrite conflicting entries
            # TODO: only do this if we're not the leader
            received_entries_iter = iter(entries)
            received_entry = next(received_entries_iter)
            for index, entry in enumerate(self.entries):
                # seek until we reach the conflict
                print(index, entry)
                if index <= prev_log_index:
                    continue
                # don't change committed entries
                if index <= self.commit_index:
                    assert self.entries[index] == entry
                if entry.term != received_entry.term:
                    assert entry.term < received_entry.term
                    # drop the conflicting entry and all that follow
                    del entry
                    while len(self.entries) > index:
                        self.entries.pop(index)
                    break
                assert entry.command == received_entry.command
                received_entry = next(received_entries_iter)
            # step 4: append new entries
            self.entries.append(received_entry)
            self.entries.extend(received_entries_iter)
        # step 5: commit as far as we now can
        if leader_commit > self.commit_index:
            self.commit_index = min(leader_commit, len(self.entries) - 1)
        print("final:", self.entries)
        return (self.current_term, True)

    def __repr__(self) -> str:
        return f"Log({self.__dict__})"
