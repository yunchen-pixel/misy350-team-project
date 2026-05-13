# Imports and Page Config

import streamlit as st
import json
from pathlib import Path
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.set_page_config(
    page_title="Broke But Up",
    layout="wide"
)

# JSON files and helper functions

users_file = Path("users.json")
listings_file = Path("listings.json")
orders_file = Path("orders.json")


def load_data(file_path):
    if file_path.exists():
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except:
            return []
    return []


def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def get_listing_emoji(listing_type):
    if listing_type == "Nails":
        return "💅"
    elif listing_type == "Henna":
        return "🌿"
    elif listing_type == "Banners":
        return "🎉"
    else:
        return "🛍️"


def show_listing(listing):
    emoji = get_listing_emoji(listing["type"])

    with st.container():
        st.markdown(f"### {emoji} {listing['name']}")
        cols = st.columns([2, 1, 1, 1])
        cols[0].write(f"Type: {listing['type']}")
        cols[1].write(f"Price: ${listing['price']}")
        cols[2].write(f"Stock: {listing['stock']}")
        cols[3].write(f"Seller: {listing['seller']}")

        if listing["stock"] < 3:
            st.warning("Low stock")

        st.divider()


def show_order(order):
    with st.container():
        st.markdown(f"**Order #{order['order_id']}**")
        cols = st.columns([2, 1, 1, 1])
        cols[0].write(f"Item: {order['item']}")
        cols[1].write(f"Qty: {order['quantity']}")
        cols[2].write(f"Total: ${order['total']}")
        cols[3].write(f"Status: {order['status']}")
        st.divider()


def show_ai_assistant():
    st.subheader("AI Assistant")
    st.write("Ask the AI assistant for help with listings, pricing, orders, or buying advice.")

    user_prompt = st.text_input("Ask the AI assistant for help:")

    if st.button("Submit Question"):
        if user_prompt:
            orders = load_data(orders_file)

            current_user = st.session_state.get("current_user")

            user_orders = [
                order for order in orders
                if order.get("buyer") == current_user
                or order.get("username") == current_user
                or order.get("buyer_username") == current_user
            ]

            if "how many orders" in user_prompt.lower():
                st.write(f"You have placed {len(user_orders)} order(s).")

            else:
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an AI assistant for Broke But Up, a student marketplace app. Help users with listings, product descriptions, pricing ideas, buying advice, and order questions."
                            },
                            {
                                "role": "user",
                                "content": user_prompt
                            }
                        ]
                    )

                    st.write(response.choices[0].message.content)

                except Exception:
                    st.error("The AI assistant is set up, but there is an OpenAI API key, billing, or quota issue.")
        else:
            st.warning("Please enter a question first.")


# Load users, listings, and orders

users = load_data(users_file)
listings = load_data(listings_file)
orders = load_data(orders_file)

# Session state set up

if "next_order_id" not in st.session_state:
    if len(orders) > 0:
        st.session_state.next_order_id = max(order["order_id"] for order in orders) + 1
    else:
        st.session_state.next_order_id = 1

if "next_listing_id" not in st.session_state:
    if len(listings) > 0:
        st.session_state.next_listing_id = max(listing["listing_id"] for listing in listings) + 1
    else:
        st.session_state.next_listing_id = 1

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "current_role" not in st.session_state:
    st.session_state.current_role = ""


# Sidebar

st.sidebar.header("Broke But Up")

if st.session_state.logged_in:
    st.sidebar.success("Logged in")
    st.sidebar.write("**User:**")
    st.sidebar.write(st.session_state.current_user)
    st.sidebar.write("**Role:**")
    st.sidebar.write(st.session_state.current_role)

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.current_role = ""
        st.rerun()
else:
    st.sidebar.info("Use the login form to continue.")

st.sidebar.divider()
st.sidebar.subheader("Test Accounts")
st.sidebar.write("Buyer: buyer / buyer123")
st.sidebar.write("Seller: seller / seller123")


# Main title

st.title("Broke But Up")
st.markdown("**Broke But Up** is a student marketplace for party and beauty items. Register, login, and manage listings and orders in one place.")


# Register and Login Area

if st.session_state.logged_in == False:

    tab1, tab2 = st.tabs([
        "Register",
        "Login"
    ])

    with tab1:
        st.subheader("Register")
        st.info("Create a new account and choose Buyer or Seller.")

        register_username = st.text_input("Create Username")
        register_password = st.text_input("Create Password", type="password")
        register_role = st.selectbox("Select Role", ["Buyer", "Seller"])

        if st.button("Register"):
            user_found = False

            for user in users:
                if user["username"] == register_username:
                    user_found = True

            if register_username == "" or register_password == "":
                st.error("Please fill in all fields")
            else:
                if user_found == True:
                    st.error("Username Already Exists")
                else:
                    new_user = {
                        "username": register_username,
                        "password": register_password,
                        "role": register_role
                    }

                    users.append(new_user)
                    save_data(users_file, users)

                    st.success("Account Created")

    with tab2:
        st.subheader("Login")
        st.info("Enter your account credentials to access the dashboard.")

        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")

        if st.button("Login"):
            valid_login = False

            for user in users:
                if user["username"] == login_username:
                    if user["password"] == login_password:
                        valid_login = True
                        st.session_state.logged_in = True
                        st.session_state.current_user = user["username"]
                        st.session_state.current_role = user["role"]

            if valid_login == True:
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Login")


# Logged in Area

if st.session_state.logged_in == True:

    st.divider()

    with st.container():
        st.subheader("Dashboard")

        cols = st.columns([2, 1])

        cols[0].write(f"**User:** {st.session_state.current_user}")
        cols[0].write(f"**Role:** {st.session_state.current_role}")

        if cols[1].button("Logout"):
            st.session_state.logged_in = False
            st.session_state.current_user = ""
            st.session_state.current_role = ""
            st.success("Logged Out")
            st.rerun()

    st.divider()

    if st.session_state.current_role == "Seller":
        my_listings = [
            listing for listing in listings
            if listing["seller"] == st.session_state.current_user
        ]

        my_orders = []

        for order in orders:
            for listing in my_listings:
                if order["item"] == listing["name"]:
                    my_orders.append(order)

        total_listings = len(my_listings)
        total_orders = len(my_orders)
        total_stock = sum(listing["stock"] for listing in my_listings)

    elif st.session_state.current_role == "Buyer":
        my_orders = [
            order for order in orders
            if order["buyer"] == st.session_state.current_user
        ]

        total_listings = len(listings)
        total_orders = len(my_orders)
        total_stock = sum(listing["stock"] for listing in listings)

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("My Listings" if st.session_state.current_role == "Seller" else "Available Listings", total_listings)
    metric2.metric("My Sales" if st.session_state.current_role == "Seller" else "My Orders", total_orders)
    metric3.metric("My Stock" if st.session_state.current_role == "Seller" else "Items in Stock", total_stock)

    st.divider()


# Seller Dashboard

    if st.session_state.current_role == "Seller":

        seller_tab1, seller_tab2, seller_tab3, seller_tab4, seller_tab5, seller_tab6 = st.tabs([
            "Create Listing",
            "View My Listings",
            "Update Listing",
            "Delete Listing",
            "Sales Summary",
            "AI Assistant"
        ])

        with seller_tab1:
            st.subheader("Create Listing")

            listing_name = st.text_input("Listing Name")
            listing_type = st.selectbox("Type", ["Nails", "Henna", "Banners"])
            listing_price = st.number_input("Price", min_value=1, step=1)
            listing_stock = st.number_input("Stock", min_value=1, step=1)

            if st.button("Create Listing"):
                if listing_name == "":
                    st.error("Please enter a listing name")
                else:
                    new_listing = {
                        "listing_id": st.session_state.next_listing_id,
                        "seller": st.session_state.current_user,
                        "name": listing_name,
                        "type": listing_type,
                        "price": listing_price,
                        "stock": listing_stock
                    }

                    listings.append(new_listing)
                    st.session_state.next_listing_id = st.session_state.next_listing_id + 1

                    save_data(listings_file, listings)

                    st.success("Listing Created")

        with seller_tab2:
            st.subheader("View My Listings")
            st.info("Your current listings are shown below.")

            listing_count = 0

            for listing in listings:
                if listing["seller"] == st.session_state.current_user:
                    show_listing(listing)
                    listing_count = listing_count + 1

            if listing_count == 0:
                st.write("No Listings")

        with seller_tab3:
            st.subheader("Update Listing")

            my_listing_names = []

            for listing in listings:
                if listing["seller"] == st.session_state.current_user:
                    my_listing_names.append(listing["name"])

            if my_listing_names == []:
                st.write("No Listings")
            else:
                selected_listing_name = st.selectbox("Select Listing", my_listing_names)
                new_price = st.number_input("New Price", min_value=1, step=1)
                new_stock = st.number_input("New Stock", min_value=0, step=1)

                if st.button("Update Listing"):
                    for listing in listings:
                        if listing["seller"] == st.session_state.current_user:
                            if listing["name"] == selected_listing_name:
                                listing["price"] = new_price
                                listing["stock"] = new_stock

                    save_data(listings_file, listings)

                    st.success("Listing Updated")

        with seller_tab4:
            st.subheader("Delete Listing")

            my_listing_names_delete = []

            for listing in listings:
                if listing["seller"] == st.session_state.current_user:
                    my_listing_names_delete.append(listing["name"])

            if my_listing_names_delete == []:
                st.write("No Listings")
            else:
                delete_listing_name = st.selectbox("Select Listing to Delete", my_listing_names_delete)

                if st.button("Delete Listing"):
                    updated_listings = []

                    for listing in listings:
                        if listing["seller"] == st.session_state.current_user and listing["name"] == delete_listing_name:
                            st.write("")
                        else:
                            updated_listings.append(listing)

                    listings = updated_listings

                    save_data(listings_file, listings)

                    st.success("Listing Deleted")

        with seller_tab5:
            st.subheader("Sales Summary")
            st.info("View sales connected to your listings.")

            seller_sales = []

            for order in orders:
                for listing in listings:
                    if order["item"] == listing["name"]:
                        if listing["seller"] == st.session_state.current_user:
                            seller_sales.append(order)

            seller_revenue = sum(order["total"] for order in seller_sales)
            seller_orders = len(seller_sales)

            col1, col2 = st.columns(2)
            col1.metric("Seller Revenue", f"${seller_revenue}")
            col2.metric("Orders Sold", seller_orders)

            st.divider()

            if seller_orders == 0:
                st.write("No sales yet.")
            else:
                for order in seller_sales:
                    show_order(order)

        with seller_tab6:
            show_ai_assistant()


# Buyer Dashboard

    if st.session_state.current_role == "Buyer":

        buyer_tab1, buyer_tab2, buyer_tab3, buyer_tab4 = st.tabs([
            "Buy Listing",
            "View Listings",
            "Manage Orders",
            "AI Assistant"
        ])

        with buyer_tab1:
            st.subheader("Buy Listing")

            item_names = []

            for listing in listings:
                if listing["stock"] > 0:
                    item_names.append(listing["name"])

            if item_names == []:
                st.write("No Listings Available")
            else:
                selected_item_name = st.selectbox("Select Item", item_names)
                quantity = st.number_input("Quantity", min_value=1, step=1)

                if st.button("Buy"):
                    selected_listing = None

                    for listing in listings:
                        if listing["name"] == selected_item_name:
                            selected_listing = listing

                    if selected_listing is not None:
                        if selected_listing["stock"] >= quantity:
                            selected_listing["stock"] = selected_listing["stock"] - quantity

                            total_price = selected_listing["price"] * quantity

                            order = {
                                "order_id": st.session_state.next_order_id,
                                "buyer": st.session_state.current_user,
                                "item": selected_listing["name"],
                                "quantity": quantity,
                                "total": total_price,
                                "status": "Placed"
                            }

                            orders.append(order)
                            st.session_state.next_order_id = st.session_state.next_order_id + 1

                            save_data(listings_file, listings)
                            save_data(orders_file, orders)

                            st.success("Order Placed")

                            with st.expander("View Receipt"):
                                st.write("Order ID")
                                st.write(order["order_id"])
                                st.write("Buyer")
                                st.write(order["buyer"])
                                st.write("Item")
                                st.write(order["item"])
                                st.write("Quantity")
                                st.write(order["quantity"])
                                st.write("Total")
                                st.write(order["total"])
                                st.write("Status")
                                st.write(order["status"])
                        else:
                            st.error("Out of Stock")

        with buyer_tab2:
            st.subheader("View Listings")
            st.info("Search or browse available items.")

            search_text = st.text_input("Search Listing Name")

            total_items_in_stock = 0

            for listing in listings:
                total_items_in_stock = total_items_in_stock + listing["stock"]

            st.write(f"Total Items in Stock: {total_items_in_stock}")
            st.divider()

            found = False

            for listing in listings:
                if search_text == "" or search_text.lower() in listing["name"].lower():
                    show_listing(listing)
                    found = True

            if not found:
                st.warning("No Listings Found")

        with buyer_tab3:
            st.subheader("Manage Orders")
            st.info("Review your orders and cancel or delete cancelled orders below.")

            order_count = 0

            for order in orders:
                if order["buyer"] == st.session_state.current_user:
                    show_order(order)
                    order_count = order_count + 1

            if order_count == 0:
                st.write("No Orders")

            cancel_order_id = st.number_input("Order ID to Cancel", min_value=1, step=1)

            if st.button("Cancel Order"):
                order_cancelled = False

                for order in orders:
                    if order["order_id"] == cancel_order_id:
                        if order["buyer"] == st.session_state.current_user:
                            if order["status"] == "Placed":
                                order["status"] = "Cancelled"
                                order_cancelled = True

                                for listing in listings:
                                    if listing["name"] == order["item"]:
                                        listing["stock"] = listing["stock"] + order["quantity"]

                                save_data(listings_file, listings)
                                save_data(orders_file, orders)

                if order_cancelled == True:
                    st.success("Order Cancelled")
                else:
                    st.error("Order could not be cancelled")

            st.subheader("Delete Cancelled Order")

            delete_order_id = st.number_input("Order ID to Delete", min_value=1, step=1, key="delete_order_id")

            if st.button("Delete Order"):
                updated_orders = []

                deleted = False

                for order in orders:
                    if order["order_id"] == delete_order_id:
                        if order["buyer"] == st.session_state.current_user and order["status"] == "Cancelled":
                            deleted = True
                        else:
                            updated_orders.append(order)
                    else:
                        updated_orders.append(order)

                if deleted == True:
                    orders = updated_orders
                    save_data(orders_file, orders)
                    st.success("Cancelled Order Deleted")
                else:
                    st.error("You can only delete your own cancelled orders")

        with buyer_tab4:
            show_ai_assistant()