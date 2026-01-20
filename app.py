from flask import Flask, request, jsonify
import services.routing_service as routing_service

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/cache/get", methods=["GET"])
def get_key(key):
    routing_service.get()
    return "<p>Request to /get</p>"

@app.route("/set", methods=["PUT"])
def set_cache_val():
    routing_service.set()
    return "<p>Request to /set</p>"

