from flask import Flask
import services.cache_client as cache_client

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get")
def get_cache_val():
    cache_client.get()
    return "<p>Request to /get</p>"

@app.route("/set")
def set_cache_val():
    cache_client.set()
    return "<p>Request to /set</p>"