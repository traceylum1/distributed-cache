import requests

class NodeClient:
    def forward_put(self, node_url: str, key: str, value: str):
        print("calling node_client forward_put")
        res = requests.put(
            f"{node_url}/cache/{key}",
            json={"value": value},
            timeout=1
        )
        return res

    def forward_get(self, node_url: str, key: str):
        print("calling node_client forward_get")
        res = requests.get(
            f"{node_url}/cache/{key}",
            timeout=1
        )
        return res