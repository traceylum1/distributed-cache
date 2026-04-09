import requests
import aiohttp
from services.cluster_service import ClusterService

class NodeClient:
    def __init__(self, cluster_service: ClusterService, retries: int):
        self.retries = retries
        self.cluster_service = cluster_service

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
        if res.status_code >= 400:
            return "", res.status_code
        else:
            return res.text, 200
    
    async def send_put_async(self, session: aiohttp.ClientSession, node_url: str, key: str, value: str):
        print("calling node_client send_put_async", node_url)
        try:
            async with session.put(url=f"{node_url}/internal/replica/{key}", json={"value": value}) as res:

                return "", res.status
        except Exception as e:
            print("Failed to set put request to replica", e.__class__)
            return "", 500
    
    def send_ping(self, node_id: str, node_url: str):
        print("calling node_client send_ping", node_url)
        try:
            res = requests.get(f"{node_url}/ping", timeout=1)
            # If we get here, the node responded
            print("Alive:", res.status_code)
            self.cluster_service.mark_alive(node_id)

        except requests.exceptions.Timeout:
            print("Timeout → node likely slow or dead")
            self.cluster_service.update_missed_pings(node_id)

        except requests.exceptions.ConnectionError as e:
            print("Connection error → node likely dead or unreachable")
            print("Details:", e)
            self.cluster_service.update_missed_pings(node_id)

        except requests.exceptions.RequestException as e:
            print("Other error:", e)
            self.cluster_service.update_missed_pings(node_id)