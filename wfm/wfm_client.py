import httpx
from typing import List
from .models import Item, Order

class WFMClient:
    def __init__(self, platform="pc"):
        self.base_url = "https://api.warframe.market/v2"
        self.headers = {
            "Platform": platform,
            "Language": "en",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }

    async def get_item(self, slug) -> Item:
        async with httpx.AsyncClient(headers=self.headers) as client:
            r = await client.get(f"{self.base_url}/items/{slug}")
            r.raise_for_status()
            return Item(**r.json()['data'])
        
    async def get_version(self):
        async with httpx.AsyncClient(headers=self.headers) as client:
            r = await client.get(f"{self.base_url}/versions")
            r.raise_for_status()
            return r.json()['apiVersion']
        
    async def get_order(self, slug) -> List[Order]:
        async with httpx.AsyncClient(headers=self.headers) as client:
            r = await client.get(f"{self.base_url}/orders/item/{slug}")
            r.raise_for_status()
            return [Order(**o) for o in r.json()['data']]