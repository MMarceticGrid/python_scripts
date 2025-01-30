
class User:
    def __init__(self, user_id, username, orders=[]):
        self.user_id = user_id  
        self.username = username  
        self.orders = orders
    
    def place_order(self, order):
        self.orders.append(order)
    

    