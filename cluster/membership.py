from models.node import NodeData, NodeConfig
from typing import List

def build_nodes(config: NodeConfig) -> List[NodeData]:
    node_map: dict[str, NodeData] = {}

    for entry in config.cluster.split(","):
        node_id, port = entry.split("=")
        is_local = node_id == config.node_id

        node_map[node_id] = NodeData(
                                id=node_id,
                                url=f"http://localhost:{port}",
                                is_local=is_local,
                                status=("alive" if is_local else "dead"),
                                missed_pings=0
                            )
    
    print("node_map", node_map)

    return node_map