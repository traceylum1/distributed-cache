from flask import Blueprint
from models.node import NodeData

def create_view_bp(node_map: dict[str, NodeData]) -> Blueprint:
    view_bp = Blueprint("view", __name__)

    @view_bp.route("/view/cluster", methods=["GET"])
    def get_view():
        return node_map

    return view_bp