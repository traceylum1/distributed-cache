# Distributed Cache

A simple **distributed in-memory cache** built with Flask that supports horizontal scaling via **consistent hashing**. Each cache node can both **receive client requests** and **forward requests to peer nodes**, allowing the system to behave as a single logical cache while being physically distributed.

This project is primarily educational and focuses on:

* Clean service boundaries
* Consistent hashing–based routing
* Node-to-node communication
* Local cache management (LRU / TTL)

---

## Features

* **Consistent Hash Ring** for key-to-node mapping
* **Local in-memory cache** per node
* **Request forwarding** between cache nodes
* Optional **TTL expiration**
* Optional **LRU eviction**
* HTTP-based API using Flask

---

## High-Level Architecture

Each cache node:

* Maintains its **own local cache**
* Knows about **all other nodes** in the cluster
* Uses the **hash ring** to determine the primary node for a key
* Either:

  * Serves the request locally, or
  * Forwards it to the appropriate peer node

Clients can send requests to **any node**.

```
Client
  │
  ▼
Cache Node A ──► Cache Node B
      │               │
      ▼               ▼
  Local Cache      Local Cache
```

---

## Project Structure

```
.
├── app.py                  # Flask app factory / entrypoint
├── cache_routes.py         # HTTP routes (GET / PUT / DELETE)
│
├── services/
│   ├── cache_service.py    # Core cache read/write logic
│   ├── routing_service.py  # Consistent hashing & node selection
│   └── eviction_service.py # LRU / TTL logic
│
├── cache/
│   └── local_cache.py      # In-memory cache implementation
│
├── clients/
│   └── node_client.py      # HTTP client for inter-node requests
│
├── config/
│   └── nodes.py            # Cluster node definitions
│
└── README.md
```

> Note: Exact structure may evolve — the key idea is that **routing**, **storage**, and **transport** remain separate concerns.

---

## API Endpoints

### Put a value

```
PUT /cache/<key>
```

**Body**

```json
{
  "value": "some-data",
  "ttl": 60
}
```

---

### Get a value

```
GET /cache/<key>
```

**Response**

```json
{
  "value": "some-data"
}
```

---

### Delete a value

```
DELETE /cache/<key>
```

---

## Consistent Hashing

* Keys are hashed onto a ring
* Each node owns one or more positions on the ring
* The **primary node** for a key is the first node clockwise from the key hash
* This minimizes key movement when nodes are added or removed

---

## Local Cache

Each node maintains its own in-memory cache:

* Dictionary-based storage
* Optional **TTL expiration**
* Optional **LRU eviction policy**

Eviction logic is isolated from routing logic to keep responsibilities clear.

---

## Running Multiple Nodes Locally

Start multiple Flask instances on different ports:

```
PORT=5001 python app.py
PORT=5002 python app.py
PORT=5003 python app.py
```

Each instance should be configured with the same node list but a different `self` identity.

---

## Configuration

Nodes are defined centrally, for example:

```python
NODES = [
    {"id": "A", "url": "http://localhost:5001"},
    {"id": "B", "url": "http://localhost:5002"},
    {"id": "C", "url": "http://localhost:5003"},
]
```

---

## Non-Goals

This project does **not** include:

* Persistence to disk
* Replication or quorum reads
* Gossip or auto-discovery
* Strong consistency guarantees

---

## Future Improvements

* Health checks & node removal
* Async request forwarding
* Metrics & observability
* Pluggable storage backends

---

## Why This Exists

This project is meant to explore **distributed systems fundamentals** in a controlled, readable codebase — not to replace Redis
