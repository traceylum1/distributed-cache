import argparse
from models.node import NodeConfig

def load_config() -> NodeConfig:
    parser = argparse.ArgumentParser(description="Distributed Cache Node")

    parser.add_argument(
        "--node-id",
        required=True,
        help="Unique node identifier (e.g. A, B, C)"
    )

    parser.add_argument(
        "--port",
        type=int,
        required=True,
        help="Port this node listens on"
    )
    
    parser.add_argument(
        "--cluster",
        required=True,
        help="Comma-separated list of node_id=port pairs (A=5000,B=5001,C=5002)"
    )

    args = parser.parse_args()

    return NodeConfig(node_id=args.node_id, port=args.port, cluster=args.cluster)