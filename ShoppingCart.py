import streamlit as st
import pandas as pd
import json
from itertools import cycle

# File paths for persistence
PRODUCTS_FILE = "products.json"
CART_FILE = "cart.json"

# Load data from files
def load_data():
    try:
        with open(PRODUCTS_FILE, "r") as f:
            st.session_state.products = json.load(f)
    except FileNotFoundError:
        st.session_state.products = {
            "Coconut Oil": {1000: 809, 500: 438, 200: 195},
            "Safflower Oil": {1000: 532, 500: 299},
            "Sunflower Oil": {1000: 410, 500: 238},
            "Groundnut Oil": {1000: 483, 500: 288},
            "Mustard Oil": {1000: 510, 500: 266, 200: 135},
            "A2 Cow Ghee": {1000: 2162, 500: 1129, 200: 594},
            "Flaxseed Oil": {500: 355, 200: 162},
            "Almond Oil": {500: 1186, 200: 495, 100: 264},
            "Castor Oil": {500: 261, 200: 124, 100: 79},
            "Kalonji Oil": {500: 1087, 200: 455, 100: 244},
            "Virgin Coconut Oil": {1000: 809, 500: 438, 200: 195},
            "Turmeric": {1000: 512, 500: 268, 250: 142},
            "Honey": {1000: 736, 500: 428, 250: 295},
            "Jaggery cubes": {1000: 152, 500: 91},
            "Jaggery powder": {1000: 194, 500: 104},
            "Brown Sugar": {1000: 225}
        }
    try:
        with open(CART_FILE, "r") as f:
            st.session_state.cart = json.load(f)
    except FileNotFoundError:
        st.session_state.cart = []

# Save data to files
def save_data():
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(st.session_state.products, f)
    with open(CART_FILE, "w") as f:
        json.dump(st.session_state.cart, f)

# Initialize session state
if 'cart' not in st.session_state or 'products' not in st.session_state:
    load_data()
if 'discount' not in st.session_state:
    st.session_state.discount = False

# Function to add item to cart
def add_to_cart(product, volume):
    st.session_state.cart.append((product, volume))
    save_data()

# Function to remove item from cart
def remove_from_cart(item):
    if item in st.session_state.cart:
        st.session_state.cart.remove(item)
        save_data()

# Function to calculate total
def calculate_total(cart, apply_discount=False):
    subtotal = sum(st.session_state.products[item][volume] for item, volume in cart)
    discount = subtotal * 0.1 if apply_discount else 0
    total = subtotal - discount
    return subtotal, discount, total

# Function to reset cart
def reset_cart():
    st.session_state.cart = []
    st.session_state.discount = False
    save_data()

# Streamlit app layout
st.title("🛒 Shopping Cart System")

# Sidebar for managing products (add/remove)
st.sidebar.header("Manage Products")
new_product_name = st.sidebar.text_input("Product Name")
new_product_price = st.sidebar.number_input("Price", min_value=0.01, format="%.2f")
if st.sidebar.button("Add Product"):
    add_product(new_product_name, new_product_price)

remove_product_name = st.sidebar.selectbox("Select a product to remove", options=list(st.session_state.products.keys()), index=0)
if st.sidebar.button("Remove Product"):
    remove_product(remove_product_name)

# Display products in a grid with volume selection
st.header("Available Products")
cols = cycle(st.columns(3))  # 3-column layout
for product, volumes in st.session_state.products.items():
    col = next(cols)
    with col:
        volume = st.selectbox(f"Select volume for {product}", options=list(volumes.keys()), key=product)
        price = volumes[volume]
        if st.button(f"{product} - Rs {price} ({volume} ml)"):
            add_to_cart(product, volume)
            st.success(f"{product} ({volume} ml) added to cart!")

# Show cart items
st.header("🛍 Your Shopping Cart")
if st.session_state.cart:
    cart_df = pd.DataFrame(st.session_state.cart, columns=["Product", "Volume (ml)"])
    st.write(cart_df)

    # Remove item dropdown
    remove_item = st.selectbox("Select an item to remove", options=st.session_state.cart, index=0)
    if st.button("Remove Item"):
        remove_from_cart(remove_item)
        st.success(f"{remove_item[0]} ({remove_item[1]} ml) removed from cart!")

    # Discount checkbox
    if st.checkbox("Apply 10% Discount"):
        st.session_state.discount = True
    else:
        st.session_state.discount = False

    # Calculate totals
    subtotal, discount, total_amount = calculate_total(st.session_state.cart, st.session_state.discount)

    # Show bill
    bill = "Bill\n"
    item_counts = {item: st.session_state.cart.count(item) for item in set(st.session_state.cart)}
    for item, count in item_counts.items():
        bill += f"- {item[0]} ({item[1]} ml) x{count}: Rs {st.session_state.products[item[0]][item[1]] * count}\n"
    bill += f"\nSubtotal: Rs{subtotal:.2f}\nDiscount: -Rs{discount:.2f}\nTotal: Rs{total_amount:.2f}"

    st.text_area("Final Bill", bill, height=200)

    # Checkout button
    if st.button("Checkout"):
        st.success("✅ Checkout successful!")

    # Reset cart button
    if st.button("Reset Cart"):
        reset_cart()
        st.warning("Cart has been reset!")

else:
    st.write("🛒 Your cart is empty.")
