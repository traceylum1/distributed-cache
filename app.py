from flask import Flask
from config import load_config
from cluster.membership import build_nodes
from services.routing_service import init_ring
from routes.cache_routes import cache_bp

def create_app():
    config = load_config()
    nodes = build_nodes(config)

    init_ring(nodes)

    app = Flask(__name__)
    app.register_blueprint(cache_bp)
    return app, config

app, config = create_app()

if __name__ == "__main__":
    app.run(port=config["port"])