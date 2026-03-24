import httpx
import asyncio
from wfm import WFMClient

async def main():
    try:
        client = WFMClient()
        version = await client.get_version()
        print(f"Current API version: {version}")                
        item_slug = "arcane_ice"
        
        '''
        item_data = await client.get_item(item_slug)
        print(f"Item data for {item_slug}: {item_data}")
        '''
        
        orders = await client.get_order(item_slug)
        #print(f"Orders for {item_slug}: {orders}")
        
        for order in orders:
            print(f"Item: {item_slug}, User: {order.user.ingame_name}, Price: {order.platinum}, Status: {order.user.status}")
        
    except httpx.HTTPStatusError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
