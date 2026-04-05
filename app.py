
import streamlit as st
import json
from pathlib import Path

st.set_page_config(
    page_title="Broke But Up",
    layout="centered"
)

st.title("Broke But Up")


# CHANGED: Added separate JSON files for users, listings, and orders

users_file = Path("users.json")
listings_file = Path("listings.json")
orders_file = Path("orders.json")


# CHANGED: Helper function to load JSON data
def load_data(file_path):
    if file_path.exists():
        with open(file_path, "r") as f:
            return json.load(f)
    return []


# CHANGED: Helper function to save JSON data
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


# CHANGED: Load users, listings, and orders from separate JSON files
users = load_data(users_file)
listings = load_data(listings_file)
orders = load_data(orders_file)

# CHANGED: Removed session_state users because users now come from JSON

# CHANGED: Removed session_state orders because orders now come from JSON

if "next_order_id" not in st.session_state:
    # CHANGED: next_order_id now continues from saved orders.json
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


tab1, tab2 = st.tabs([
    "Register",
    "Login"
])

with tab1:
    st.subheader("Register")

    register_username = st.text_input("Create Username")
    register_password = st.text_input("Create Password")
    register_role = st.selectbox("Select Role", ["Buyer", "Seller"])

    if st.button("Register"):
        user_found = False

        # CHANGED: Check users from users.json instead of session_state
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

                # CHANGED: Save new users to users.json
                users.append(new_user)
                save_data(users_file, users)

                st.success("Account Created")

with tab2:
    st.subheader("Login")

    login_username = st.text_input("Username")
    login_password = st.text_input("Password")

    if st.button("Login"):
        valid_login = False

        # CHANGED: Check login using users from users.json
        for user in users:
            if user["username"] == login_username:
                if user["password"] == login_password:
                    valid_login = True
                    st.session_state.logged_in = True
                    st.session_state.current_user = user["username"]
                    st.session_state.current_role = user["role"]

        if valid_login == True:
            st.success("Login Successful")
        else:
            st.error("Invalid Login")


if st.session_state.logged_in == True:
    st.write("Logged In User")
    st.write(st.session_state.current_user)
    st.write("Role")
    st.write(st.session_state.current_role)

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = ""
        st.session_state.current_role = ""
        st.success("Logged Out")


    if st.session_state.current_role == "Seller":
        seller_tab1, seller_tab2, seller_tab3, seller_tab4 = st.tabs([
            "Create Listing",
            "View My Listings",
            "Update Listing",
            "Delete Listing"
        ])

        with seller_tab1:
            st.subheader("Create Listing")

            listing_name = st.text_input("Listing Name")
            listing_type = st.selectbox("Type", ["Nails", "Henna", "Banners"])
            listing_price = st.number_input("Price", min_value=1, step=1)
            listing_stock = st.number_input("Stock", min_value=1, step=1)

            if st.button("Create Listing"):
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

                # CHANGED: Save listings to listings.json
                save_data(listings_file, listings)

                st.success("Listing Created")

        with seller_tab2:
            st.subheader("View My Listings")

            for listing in listings:
                if listing["seller"] == st.session_state.current_user:
                    if listing["stock"] < 3:
                        st.warning(listing)
                    else:
                        st.write(listing)

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

                    # CHANGED: Save updated listings to listings.json
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

                    # CHANGED: Save deleted listings to listings.json
                    save_data(listings_file, listings)

                    st.success("Listing Deleted")


    if st.session_state.current_role == "Buyer":
        buyer_tab1, buyer_tab2, buyer_tab3 = st.tabs([
            "Buy Listing",
            "View Listings",
            "Manage Orders"
        ])

        with buyer_tab1:
            st.subheader("Buy Listing")

            item_names = []

            for listing in listings:
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

                            # CHANGED: Save orders to orders.json instead of session_state
                            orders.append(order)
                            st.session_state.next_order_id = st.session_state.next_order_id + 1

                            # CHANGED: Save both listings and orders after purchase
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

            search_text = st.text_input("Search Listing Name")

            total_items_in_stock = 0

            for listing in listings:
                total_items_in_stock = total_items_in_stock + listing["stock"]

            st.write("Total Items in Stock")
            st.write(total_items_in_stock)

            st.write("Listings")

            for listing in listings:
                if search_text == "":
                    if listing["stock"] < 3:
                        st.warning(listing)
                    else:
                        st.write(listing)
                else:
                    if search_text == listing["name"]:
                        if listing["stock"] < 3:
                            st.warning(listing)
                        else:
                            st.write(listing)

        with buyer_tab3:
            st.subheader("Manage Orders")

            st.write("Orders")

            # CHANGED: Read orders from orders.json instead of session_state
            for order in orders:
                if order["buyer"] == st.session_state.current_user:
                    st.write(order)

            cancel_order_id = st.number_input("Order ID to Cancel", min_value=1, step=1)

            if st.button("Cancel Order"):
                # CHANGED: Update orders from orders.json instead of session_state
                for order in orders:
                    if order["order_id"] == cancel_order_id:
                        if order["buyer"] == st.session_state.current_user:
                            if order["status"] == "Placed":
                                order["status"] = "Cancelled"

                                for listing in listings:
                                    if listing["name"] == order["item"]:
                                        listing["stock"] = listing["stock"] + order["quantity"]

                                # CHANGED: Save updated listings and orders after cancellation
                                save_data(listings_file, listings)
                                save_data(orders_file, orders)

                                st.success("Order Cancelled")