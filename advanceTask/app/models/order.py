from datetime import datetime

class Order:
    def __init__(self, order_id, user_id, pizzas=None, status='not_ready_to_be_delivered'):
        self.order_id = order_id
        self.user_id = user_id
        self.pizzas = pizzas if pizzas else [] 
        self.status = status
        self.created_at = datetime.now()


    def add_pizza(self, pizza):
        self.pizzas.append(pizza)
    
    def remove_pizza(self, pizza_id):
        self.pizzas = [pizza for pizza in self.pizzas if pizza.pizza_id != pizza_id]
    
    def total_price(self):
        return sum(pizza.price for pizza in self.pizzas)
    