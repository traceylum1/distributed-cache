import requests

class NodeClient:
    def send_put(node_url: str, key: str, value: str):
        print("calling node_client send_put")
        return requests.put(
            f"{node_url}/cache/{key}",
            json={"value": value},
            timeout=1
        )

    def send_get(node_url: str, key: str):
        print("calling node_client send_get")
        return requests.get()