
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from datetime import datetime
import os
# Load environment variables from .env file
load_dotenv()

# MongoDB connection setup using environment variables
client = MongoClient(os.getenv("MONGODB_URI"))
db = client[os.getenv("DATABASE_NAME")]

# MongoDB collections
orders_collection = db["orders"]
order_items_collection = db["order_items"]
order_tracking_collection = db["order_tracking"]

# Function to insert an order item
def insert_order_item(food_item, quantity, order_id):
    try:
        # Check if the order exists
        order = orders_collection.find_one({"_id": ObjectId(order_id)})
        if not order:
            print(f"Order with ID {order_id} does not exist!")
            return -1

        # Insert order item
        order_item = {
            "food_item": food_item,
            "quantity": quantity,
            "order_id": ObjectId(order_id),
            "created_at": datetime.now()
        }
        order_items_collection.insert_one(order_item)
        print("Order item inserted successfully!")
        return 1

    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

# Function to insert a record into the order_tracking collection
def insert_order_tracking(order_id, status):
    try:
        # Insert tracking information
        order_tracking = {
            "order_id": ObjectId(order_id),
            "status": status,
            "updated_at": datetime.now()
        }
        order_tracking_collection.insert_one(order_tracking)
        print("Order tracking inserted successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to calculate the total price of an order
def get_total_order_price(order_id):
    try:
        # Fetch all order items for the given order ID
        items = order_items_collection.find({"order_id": ObjectId(order_id)})
        total_price = 0

        # Example: Assume each item has a "price" field
        for item in items:
            total_price += item.get("price", 0) * item.get("quantity", 0)
        return total_price
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0

# Function to get the next available order_id
def get_next_order_id():
    try:
        # Create a new order and get its unique ID
        new_order = {"created_at": datetime.now()}
        result = orders_collection.insert_one(new_order)
        return str(result.inserted_id)  # Return the new order ID as a string
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to fetch the order status from the order_tracking collection
def get_order_status(order_id):
    try:
        # Fetch the latest status for the given order ID
        status_record = order_tracking_collection.find_one(
            {"order_id": ObjectId(order_id)},
            sort=[("updated_at", -1)]  # Sort by the latest updated_at timestamp
        )
        if status_record:
            return status_record["status"]
        else:
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Create a new order and get the order ID
    order_id = get_next_order_id()
    print(f"New Order ID: {order_id}")

    # Insert order items
    insert_order_item("Samosa", 3, order_id)
    insert_order_item("Pav Bhaji", 1, order_id)

    # Insert order tracking
    insert_order_tracking(order_id, "in progress")

    # Get total order price
    total_price = get_total_order_price(order_id)
    print(f"Total Order Price: {total_price}")

    # Get order status
    status = get_order_status(order_id)
    print(f"Order Status: {status}")
