import requests

class NodeClient:
    def forward_put(self, node_url: str, key: str, value: str):
        print("calling node_client forward_put")
        res = requests.put(
            f"{node_url}/internal/cache/{key}",
            json={"value": value},
            timeout=1
        )
        return "", res.status_code

    def forward_get(self, node_url: str, key: str):
        print("calling node_client forward_get")
        res = requests.get(
            f"{node_url}/internal/cache/{key}",
            timeout=1
        )
        if res.status_code > 400:
            return "", res.status_code
        else:
            return res.text, 200