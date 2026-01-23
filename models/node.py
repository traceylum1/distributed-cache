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