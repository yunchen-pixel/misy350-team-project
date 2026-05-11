import json
from pathlib import Path
from models import User, Listing, Order

users_file = Path("users.json")
listings_file = Path("listings.json")
orders_file = Path("orders.json")


def load_data(file_path):
    # ADDED: Return an empty list if file is missing or invalid
    if file_path.exists():
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_data(file_path, data):
    # CHANGED: Keep JSON nice and readable with indent=4
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_users():
    return load_data(users_file)


def load_listings():
    return load_data(listings_file)


def load_orders():
    return load_data(orders_file)


def save_users(users):
    save_data(users_file, users)


def save_listings(listings):
    save_data(listings_file, listings)


def save_orders(orders):
    save_data(orders_file, orders)


def seed_sample_data():
    # ADDED: Create default sample data only when files are empty or missing
    users = load_users()
    listings = load_listings()
    orders = load_orders()

    if users == []:
        sample_users = [
            User("buyer1", "buyer123", "Buyer").to_dict(),
            User("seller1", "seller123", "Seller").to_dict()
        ]
        save_users(sample_users)

    if listings == []:
        sample_listings = [
            Listing(1, "testseller", "Party Banner", "Banners", 20, 5).to_dict(),
            Listing(2, "testseller", "Henna Art", "Henna", 15, 3).to_dict()
        ]
        save_listings(sample_listings)

    if orders == []:
        save_orders([])
