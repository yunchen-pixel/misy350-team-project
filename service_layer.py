# ADDED: Service layer for business logic functions


def find_user(users, username):
    for user in users:
        if user["username"] == username:
            return user
    return None


def username_exists(users, username):
    for user in users:
        if user["username"] == username:
            return True
    return False


def validate_login(users, username, password):
    for user in users:
        if user["username"] == username:
            if user["password"] == password:
                return True
    return False


def get_user_listings(listings, seller_username):
    seller_listings = []
    for listing in listings:
        if listing["seller"] == seller_username:
            seller_listings.append(listing)
    return seller_listings


def get_buyer_orders(orders, buyer_username):
    buyer_orders = []
    for order in orders:
        if order["buyer"] == buyer_username:
            buyer_orders.append(order)
    return buyer_orders


def find_listing_by_name(listings, listing_name):
    for listing in listings:
        if listing["name"] == listing_name:
            return listing
    return None


def update_listing(listings, seller_username, listing_name, new_price, new_stock):
    updated = False
    for listing in listings:
        if listing["seller"] == seller_username and listing["name"] == listing_name:
            listing["price"] = new_price
            listing["stock"] = new_stock
            updated = True
    return updated


def delete_listing(listings, seller_username, listing_name):
    updated_listings = []
    deleted = False
    for listing in listings:
        if listing["seller"] == seller_username and listing["name"] == listing_name and deleted == False:
            deleted = True
        else:
            updated_listings.append(listing)
    return updated_listings, deleted


def cancel_order(orders, listings, buyer_username, order_id):
    cancelled = False
    for order in orders:
        if order["order_id"] == order_id:
            if order["buyer"] == buyer_username and order["status"] == "Placed":
                order["status"] = "Cancelled"
                for listing in listings:
                    if listing["name"] == order["item"]:
                        listing["stock"] = listing["stock"] + order["quantity"]
                cancelled = True
                break
    return cancelled


def delete_cancelled_order(orders, buyer_username, order_id):
    updated_orders = []
    deleted = False
    for order in orders:
        if order["order_id"] == order_id and order["buyer"] == buyer_username and order["status"] == "Cancelled":
            deleted = True
        else:
            updated_orders.append(order)
    return updated_orders, deleted
