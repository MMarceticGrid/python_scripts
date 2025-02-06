#!/Users/mmarcetic/Documents/python3_course/practical_python/advanceTask/env/bin/python3

import argparse
import requests
import sys

def list_menu():
    response = requests.get("http://127.0.0.1:5000/menu")

    if response.status_code == 200:
        print("Menu:")
        print(response.text)
    else:
        print(response.json())
        sys.exit(1)

def create_order(user_id, pizzas):
    payload = {
        "user_id" : user_id,
        "pizzas" : pizzas
    }
    response = requests.post("http://127.0.0.1:5000/order", json=payload)

    if response.status_code == 201:
        print("Order created successfully!")
        print(f"Order ID: {response.json()['order_id']}")
    else:
        print(response.json())
        sys.exit(1)

def check_order_status(order_id):
    response = requests.get(f"http://127.0.0.1:5000/order/{order_id}")
    if response.status_code == 200:
        print(f"Order ID: {response.json()['order_id']}")
        print(f"Order Status: {response.json()['status']}")
    else:
        print(response.json())
        sys.exit(1)

def cancel_order(order_id):
    response = requests.delete(f"http://127.0.0.1:5000/order/{order_id}")
    if response.status_code == 200:
        print(f"Order ID: {response.json()['order_id']}")
        print(f"{response.json()['message']}")
    else:
        print(response.json())
        sys.exit(1)

def add_pizza(name,description, price, admin_token):

    if admin_token:
        headers = {
            "Authorization" : f"Bearer {admin_token}"
        }

    payload = {
        "name" : name,
        "description": description,
        "price" : price
    }
    response = requests.post("http://127.0.0.1:5000/admin/menu", headers=headers,json=payload)
    if response.status_code == 201:
        print("Pizza added successfully!")
        print(f"Pizza ID: {response.json()['pizza_id']}")
    elif response.status_code == 401:
        print("Unauthorized : Invalid admin token.")
        sys.exit(1)
    else:
        print(response.json())
        sys.exit(1)


def delete_pizza(pizza_id, admin_token):
    if admin_token:
        headers = {
            "Authorization" : f"Bearer {admin_token}"
        }
    response = requests.delete(f"http://127.0.0.1:5000/admin/menu/{pizza_id}", headers=headers)
    if response.status_code == 200:
        print("Pizza deleted successfully from menu!")
        print(f"Pizza ID: {response.json()['pizza_id']}")
    elif response.status_code == 401:
        print("Unauthorized : Invalid admin token.")
        sys.exit(1)
    else:
        print(response.json())
        sys.exit(1)


def cancel_order_admin(order_id, admin_token):
    if admin_token:
        headers = {
            "Authorization" : f"Bearer {admin_token}"
        }
    response = requests.delete(f"http://127.0.0.1:5000/admin/order/{order_id}", headers=headers)
    if response.status_code == 200:
        print("Order canceled successfully!")
        print(f"Order ID: {response.json()['order_id']}")
    elif response.status_code == 401:
        print("Unauthorized : Invalid admin token.")
        sys.exit(1)
    else:
        print(response.json())
        sys.exit(1)

def update_order_status(order_id, status, admin_token):
    if admin_token:
        headers = {
            "Authorization" : f"Bearer {admin_token}"
        }
        payload = {
            "status" : status
        }
    response = requests.put(f"http://127.0.0.1:5000/admin/order/{order_id}", headers=headers, json=payload)
    if response.status_code == 200:
        print("Order status updated successfully!")
        print(f"Order ID: {response.json()['order_id']}, New status: {response.json()['status']}")
    elif response.status_code == 401:
        print("Unauthorized : Invalid admin token.")
        sys.exit(1)
    else:
        print(response.json())
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Customer CLI for ordering")
    parser.add_argument('--role', choices=['customer', 'admin'], required=True, help="Role of the user")
    subparsers = parser.add_subparsers(dest="command")

    #Command to list the menu
    subparsers.add_parser("list-menu", help="List the available menu items")
    
    # Command to create an order
    create_order_parser = subparsers.add_parser("create-order", help="Create a new order (e.g., create-order user_id pizzas_id)")
    create_order_parser.add_argument("user_id", type=int, help="User ID to associate with the order")
    create_order_parser.add_argument("items", metavar="item_id", type=int, nargs="+", help="Item IDs to add to the order")
    
    # Command to check order status
    check_order_parser = subparsers.add_parser("check-order", help="Check the status of an order (e.g., check-order order_id)")
    check_order_parser.add_argument("order_id", type=int, help="Order ID to check the status")
    
    # Command to cancel an order
    cancel_order_parser = subparsers.add_parser("cancel-order", help="Cancel an order (e.g., cancel-order order_id)")
    cancel_order_parser.add_argument("order_id", type=int, help="Order ID to cancel")

    #Command to add pizza to menu
    add_pizza_parser = subparsers.add_parser("add-pizza", help="Add pizza in menu (e.g., add-pizza name description price)")
    add_pizza_parser.add_argument("name", help="Pizza name")
    add_pizza_parser.add_argument("description", help="Description represent all ingredients")
    add_pizza_parser.add_argument("price", type=float, help="Pizza price")
    add_pizza_parser.add_argument("admin_token", help="Admin token for authorization")

    # Command to delete pizza from menu
    delete_pizza_parser = subparsers.add_parser("delete-pizza", help="Delete pizza from menu (e.g., delete-pizza pizza_id)")
    delete_pizza_parser.add_argument("pizza_id", type=int, help="Pizza ID to delete")
    delete_pizza_parser.add_argument("admin_token", help="Admin token for authorization")

    # Command to cancel order regardless of status
    cancel_order_admin_parser = subparsers.add_parser("cancel-order-admin", help="Cancel order regardless of status (e.g., cancel-order-admin order_id)")
    cancel_order_admin_parser.add_argument("order_id", type=int, help="Order ID to delete")
    cancel_order_admin_parser.add_argument("admin_token", help="Admin token for authorization")

    #Command to update order status
    update_order_status_parser = subparsers.add_parser("update-order-status", help="Update order status (e.g., update-order-status order_id new_status)")
    update_order_status_parser.add_argument("order_id", type=int, help="Order ID")
    update_order_status_parser.add_argument("new_status", help="New order status")
    update_order_status_parser.add_argument("admin_token", help="Admin token for authorization")
    args = parser.parse_args()

    if args.command == "list-menu":
        list_menu()
    elif args.command == "create-order":
        create_order(args.user_id ,args.items)
    elif args.command == "check-order":
        check_order_status(args.order_id)
    elif args.command == "cancel-order":
        cancel_order(args.order_id)
    elif args.role == "admin":
        if args.command == "add-pizza":
            add_pizza(args.name, args.description, args.price, args.admin_token)
        elif args.command == "delete-pizza":
            delete_pizza(args.pizza_id, args.admin_token)
        elif args.command == "cancel-order-admin":
            cancel_order_admin(args.order_id, args.admin_token)
        elif args.command == "update-order-status":
            update_order_status(args.order_id, args.new_status, args.admin_token)
    else:
        print("Invalid command. Use --help for usage instructions.")
        print("As a customer you can execute (list-menu, create-order, cancel-order, check-order)")
    

if __name__ == "__main__":
    main()

