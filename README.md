# pythonfoo-raft

We're currently re-implementing [raft](https://raft.github.io/) at @Pythonfoo.

This is my implementation.

## current state

We do have a single-node key-value store and a client accessing it.
Also, tests for both.

## running

server:

```
python3 -m raft.server.server
```

client:

```
python3 -m raft.client.cli
```
