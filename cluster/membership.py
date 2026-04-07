from models.node import NodeData, NodeConfig
from typing import List

def build_nodes(config: NodeConfig) -> List[NodeData]:
    nodes = []

    for entry in config.cluster.split(","):
        node_id, port = entry.split("=")

        nodes.append(
            NodeData(
                id=node_id,
                url=f"http://localhost:{port}",
                is_local=(node_id == config.node_id),
                status="alive",
                missed_pings=0
            )
        )
    print("nodes", nodes)

    return nodes