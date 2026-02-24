from typing import List
from models.node import Node
from clients.node_client import NodeClient
import aiohttp
import asyncio

async def replicate_to(node_client: NodeClient, replicas: List[Node], key: str, value: str):
    print("calling node_client replicate_to")
    try:
        async with aiohttp.ClientSession() as session:
            await asyncio.gather(*(node_client.send_put_async(session, r.url, key, value) for r in replicas))
        print("Sent all requests")

    except Exception as e:
        print("Error with replication requests", e.__class__)