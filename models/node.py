from dataclasses import dataclass

@dataclass(fronzen=True)
class Node:
    id: str
    url: str
    is_local: bool