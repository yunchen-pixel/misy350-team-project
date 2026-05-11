# ADDED: Models file for Phase 2 OOP evidence

class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role
        }


class Listing:
    def __init__(self, listing_id, seller, name, listing_type, price, stock):
        self.listing_id = listing_id
        self.seller = seller
        self.name = name
        self.type = listing_type
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "listing_id": self.listing_id,
            "seller": self.seller,
            "name": self.name,
            "type": self.type,
            "price": self.price,
            "stock": self.stock
        }


class Order:
    def __init__(self, order_id, buyer, item, quantity, total, status):
        self.order_id = order_id
        self.buyer = buyer
        self.item = item
        self.quantity = quantity
        self.total = total
        self.status = status

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "buyer": self.buyer,
            "item": self.item,
            "quantity": self.quantity,
            "total": self.total,
            "status": self.status
        }
