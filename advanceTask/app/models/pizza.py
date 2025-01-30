
class Pizza:
    def __init__(self, pizza_id, name, description, price):
        self.pizza_id = pizza_id  
        self.name = name 
        self.description = description  
        self.price = price
    
    def __str__(self):
        return f"Pizza {self.pizza_id}: Name={self.name}, Toppings={', '.join(self.description)}, Price=${self.price:.2f}"
    
    def update_price(self, price):
        self.price = price

