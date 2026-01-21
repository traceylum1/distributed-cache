import requests

def send_put(node_url: str, key: str, value: str):
    return requests.put(
        f"{node_url}/cache/{key}",
        json={"value": value},
        timeout=1
    )

# def send_get(node.url, key):
#     return requests.get()