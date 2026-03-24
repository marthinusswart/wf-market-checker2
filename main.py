import httpx
import asyncio
import json
from wfm import WFMClient
from wfm.alert import Alert
from wfm.alert_manager import AlertManager

def load_alerts_from_json(filename, alert_manager):
    try:
        with open(filename, 'r') as f:
            alerts_data = json.load(f)['alerts']
            for alert_data in alerts_data:
                alert = Alert(item_slug=alert_data['item_slug'], max_price=alert_data['max_price'])
                if 'rank' in alert_data:
                    alert.rank = alert_data['rank']
                alert_manager.add_alert(alert)
        print(f"Loaded alerts from {filename}")
    except FileNotFoundError:
        print(f"Alert file {filename} not found.")
    except Exception as e:
        print(f"Error loading alerts: {e}")

async def check_orders(client, tracked_items, alert_manager):
    for item_slug in tracked_items:
        try:
            orders = await client.get_order(item_slug)
            orders.sort(key=lambda o: o.platinum)  # Sort orders by price

            # Filter alerts for the current item to avoid false positives from other items
            relevant_alerts = [a for a in alert_manager.get_alerts() if a.item_slug == item_slug]

            print("===============================================================") 
            print(f"Checking orders for {item_slug}")
            print("===============================================================") 
            
            for order in orders:
                if any(alert.check_condition(order) for alert in relevant_alerts):
                    print(f"Alert triggered User: {order.user.ingame_name}, Rank: {order.rank}, Price: {order.platinum}, Status: {order.user.status}")
        except httpx.HTTPStatusError as e:
            print(f"Error fetching orders for {item_slug}: {e}")

async def main():
    try:
        client = WFMClient()
        alert_manager = AlertManager()
        load_alerts_from_json("alerts.json", alert_manager)
        
        version = await client.get_version()
        print(f"Current API version: {version}")                        
        
        tracked_items = set(alert.item_slug for alert in alert_manager.get_alerts())
        
        while True:
            await check_orders(client, tracked_items, alert_manager)
            print("Waiting for 60 seconds before the next check...")
            await asyncio.sleep(60)

    except httpx.HTTPStatusError as e:
        print(f"An HTTP error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
