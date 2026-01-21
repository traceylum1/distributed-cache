from dataclasses import dataclass

@dataclass(frozen=True)
class Node:
    id: str
    url: str
    is_local: bool