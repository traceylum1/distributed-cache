from models.node import Node, NodeConfig
from typing import List

def build_nodes(config: NodeConfig) -> List[Node]:
    nodes = []

    for entry in config.cluster.split(","):
        node_id, port = entry.split("=")

        nodes.append(
            Node(
                id=node_id,
                url=f"http://localhost:{port}",
                is_local=(node_id == config.node_id)
            )
        )
    print("nodes", nodes)

    return nodes