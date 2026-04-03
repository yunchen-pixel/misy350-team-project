import streamlit as st
import json
from pathlib import Path

json_file = Path("inventory.json")

if json_file.exists():
    with open(json_file, "r") as f:
        inventory = json.load(f)
else:
    # Default data if file doesn't exist
    inventory = [] 

if "orders" not in st.session_state:
    st.session_state.orders = []
    
tab1, tab2, tab3, tab4 = st.tabs([
    "Place Order",
    "View Inventory",
    "Restock",
    "Manage Orders"
])

st.title("Broke But Up")