from .models import Order

class Alert:
    def __init__(self, item_slug: str, max_price: int, rank: int = 0):
        self.item_slug = item_slug
        self.max_price = max_price
        self.rank = rank

    def check_condition(self, order: Order) -> bool:
        """
        Checks if a specific order meets the alert criteria.
        """
        if order.type != "sell":
            return False
        
        if order.platinum > self.max_price:
            return False
            
        if order.user.status != "ingame":
            return False
        
        if order.rank < self.rank:
            return False
            
        return True

    def __repr__(self):
        return f"Alert(item={self.item_slug}, max_price={self.max_price})"
