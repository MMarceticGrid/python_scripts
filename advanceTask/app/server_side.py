#!/Users/mmarcetic/Documents/python3_course/practical_python/advanceTask/env/bin/python3

from flask import Flask, request, jsonify
from models.pizza import Pizza
from models.user import User
from models.order import Order
from datetime import datetime
from flask_httpauth import HTTPTokenAuth
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
orders_db = []

auth = HTTPTokenAuth(scheme='Bearer')
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN')

# Token verification function
@auth.verify_token
def verify_token(token):
    return token == ADMIN_TOKEN

pizzas_db = [
    Pizza(1, "Capicciosa", "Pizza dough, Tomato sauce, Mozzarella cheese, Ham, Mushrooms", 15.99),
    Pizza(2, "Pepperoni", "Pizza dough, Tomato sauce, Mozzarella cheese, Ham, Pepperoni", 12.49),
    Pizza(3, "Vesuvio", "Pizza dough, Tomato sauce, Fresh mozzarella cheese, Fresh basil leaves", 9.99)
]

users_db = [
    User(1, "john_doe"),
    User(2, "jane_smith")
]

# Function to get a pizza by ID
def get_pizza_by_id(pizza_id):
    return next((pizza for pizza in pizzas_db if pizza.pizza_id == pizza_id), None)

# Function to get an order by ID
def get_order_by_id(order_id):
    return next((order for order in orders_db if order.order_id == order_id), None)

#Function to get an user by ID
def get_user_by_id(user_id):
    return next((user for user in users_db if user.user_id == user_id), None)

@app.route('/menu', methods=['GET'])
def list_menu():
    menu = [pizza.__dict__ for pizza in pizzas_db]
    return jsonify(menu)
@app.route('/order', methods=['POST'])
def create_order():
    data = request.get_json()

    # Example JSON data format: {"user_id": 1, "pizzas": [1, 2]}
    user_id = data.get("user_id")
    pizza_ids = data.get("pizzas", [])
    
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    pizzas_in_order = []
    for pizza_id in pizza_ids:
        pizza = get_pizza_by_id(pizza_id)
        if pizza:
            pizzas_in_order.append(pizza)
        else:
            return jsonify({"error": f"Pizza with ID {pizza_id} not found"}), 404
    
    order_id = len(orders_db) + 1
    order = Order(order_id, user_id, pizzas_in_order, status="not_ready_to_be_delivered")
    orders_db.append(order)
    user.place_order(order)
    
    return jsonify({"message": "Order created successfully", "order_id": order_id}), 201

# Endpoint to check order status (GET /order/{order_id})
@app.route('/order/<int:order_id>', methods=['GET'])
def check_order_status(order_id):
    order = get_order_by_id(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify({"order_id": order_id, "status": order.status})


@app.route('/order/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    order = get_order_by_id(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    if order.status == "ready_to_be_delivered":
        return jsonify({"error": "Order is ready to be delivered and cannot be cancelled"}), 400
    
    # Remove order from the user's order history
    user = get_user_by_id(order.user_id)
    user.orders = [o for o in user.orders if o.order_id != order_id]

    orders_db.remove(order)
    
    return jsonify({"order_id": order_id,"message": "Order cancelled successfully"})

@app.route('/admin/menu', methods=['POST'])
@auth.login_required
def add_pizza():
    data = request.get_json()

    pizza_id = len(pizzas_db) + 1
    pizza = Pizza(pizza_id,data.get('name'), data.get('description'),data.get('price'))
    pizzas_db.append(pizza)

    return jsonify({"message": "Pizza added successfully", "pizza_id": pizza_id}), 201

@app.route('/admin/menu/<int:pizza_id>', methods=['DELETE'])
@auth.login_required
def delete_pizza(pizza_id):
    pizza = get_pizza_by_id(pizza_id)

    if not pizza:
        return jsonify({"error": f"Pizza with id {pizza_id} doesn't exist in menu"}), 404
    
    pizzas_db.remove(pizza)
    return jsonify({"message": "Pizza is successfully deleted from menu", "pizza_id": pizza_id})

@app.route('/admin/order/<int:order_id>', methods=['DELETE'])
@auth.login_required
def delete_order(order_id):
    order = get_order_by_id(order_id)

    if not order:
        return jsonify({"error": f"Order with id {order_id} doesn't exist."}), 404
    
    orders_db.remove(order)
    return jsonify({"message": "Order is successfully deleted from menu", "order_id" : order_id})

@app.route('/admin/order/<int:order_id>', methods=['PUT'])
@auth.login_required
def update_status(order_id):
    data = request.get_json()
    status = data.get("status")
    
    if status not in ["ready_to_be_delivered", "not_ready_to_be_delivered"]:
        return jsonify({
            "error": "Order status must be one of the following options: 'ready_to_be_delivered' or 'not_ready_to_be_delivered'."
        }), 400
    
    order = get_order_by_id(order_id)

    if not order:
        return jsonify({"error": f"Order with id {order_id} doesn't exist."}), 404

    old_status = order.status
    order.status = status
    
    return jsonify({"message": f"Order status is successfully update from '{old_status}' to '{status}'",
                   "order_id" : order_id , "status" : status}),200
    
    

if __name__ == "__main__":
    app.run(debug=True)
