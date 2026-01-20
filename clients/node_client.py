import requests

def send_put(node_url, key, value):
    return requests.put(
        f"{node_url}/cache/{key}",
        json={"value": value},
        timeout=1
    )