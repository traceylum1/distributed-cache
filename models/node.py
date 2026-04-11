from dataclasses import dataclass

@dataclass(frozen=True)
class Node:
    id: str
    url: str
    is_local: bool

@dataclass(frozen=True)
class NodeConfig:
    node_id: str
    port: int
    cluster: str

@dataclass
class NodeState:
    status: str
    missed_pings: int

@dataclass
class NodeData:
    id: str
    url: str
    is_local: bool
    status: str
    missed_pings: int
    last_ping: float
    backoff_interval: int