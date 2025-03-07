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
            "Coconut Oil 1 l": 809, "Coconut Oil 500 ml": 438, "Coconut Oil 200 ml": 195,
            "Safflower Oil 1 l": 532, "Safflower Oil 500 ml": 299,
            "Sunflower Oil 1 l": 410, "Sunflower Oil 500 ml": 238,
            "Groundnut Oil 1 l": 483, "Groundnut Oil 500 ml": 288,
            "Mustard Oil 1 l": 510, "Mustard Oil 500 ml": 266, "Mustard Oil 200 ml": 135,
            "A2 Cow Ghee 1 kg": 2162, "A2 Cow Ghee 500 g": 1129, "A2 Cow Ghee 200 g": 594,
            "Flaxseed Oil 500 ml": 355, "Flaxseed Oil 200 ml": 162,
            "Almond Oil 500 ml": 1186, "Almond Oil 200 ml": 495, "Almond Oil 100 ml": 264,
            "Castor Oil 500 ml": 261, "Castor Oil 200 ml": 124, "Castor Oil 100 ml": 79,
            "Kalonji Oil 500 ml": 1087, "Kalonji Oil 200 ml": 455, "Kalonji Oil 100 ml": 244,
            "Virgin Coconut Oil 1 l": 809, "Virgin Coconut Oil 500 ml": 438, "Virgin Coconut Oil 200 ml": 195,
            "Turmeric 1 kg": 512, "Turmeric 500 g": 268, "Turmeric 250 g": 142,
            "Honey 1 kg": 736, "Honey 500 g": 428, "Honey 250 g": 295,
            "Jaggery cubes 1 kg": 152, "Jaggery cubes 500 g": 91,
            "Jaggery powder 1 kg": 194, "Jaggery powder 500 g": 104,
            "Brown Sugar 1 kg": 225
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
def add_to_cart(product):
    st.session_state.cart.append(product)
    save_data()

# Function to remove item from cart
def remove_from_cart(product):
    if product in st.session_state.cart:
        st.session_state.cart.remove(product)
        save_data()

# Function to calculate total
def calculate_total(cart, apply_discount=False):
    subtotal = sum(st.session_state.products[item] for item in cart)
    discount = subtotal * 0.1 if apply_discount else 0
    total = subtotal - discount
    return subtotal, discount, total

# Function to reset cart
def reset_cart():
    st.session_state.cart = []
    st.session_state.discount = False
    save_data()

# Function to add new product
def add_product(name, price):
    if name and price > 0:
        st.session_state.products[name] = price
        save_data()
        st.success(f"{name} added at ${price}")

# Function to remove a product
def remove_product(name):
    if name in st.session_state.products:
        del st.session_state.products[name]
        save_data()
        st.success(f"{name} removed from products")

# Streamlit app layout
st.title("🛒 Shopping Cart System")

# Sidebar for adding/removing products
st.sidebar.header("Manage Products")
new_product_name = st.sidebar.text_input("Product Name")
new_product_price = st.sidebar.number_input("Price", min_value=0.01, format="%.2f")
if st.sidebar.button("Add Product"):
    add_product(new_product_name, new_product_price)

remove_product_name = st.sidebar.selectbox("Select a product to remove", options=list(st.session_state.products.keys()), index=0)
if st.sidebar.button("Remove Product"):
    remove_product(remove_product_name)

# Display products in a grid
st.header("Available Products")
cols = cycle(st.columns(3))  # 3-column layout
for product, price in st.session_state.products.items():
    col = next(cols)
    with col:
        if st.button(f"{product} - Rs {price}"):
            add_to_cart(product)
            st.success(f"{product} added to cart!")

# Show cart items
st.header("🛍 Your Shopping Cart")
if st.session_state.cart:
    cart_df = pd.DataFrame(st.session_state.cart, columns=["Items"])
    st.write(cart_df)

    # Remove item dropdown
    remove_item = st.selectbox("Select an item to remove", options=st.session_state.cart, index=0)
    if st.button("Remove Item"):
        remove_from_cart(remove_item)
        st.success(f"{remove_item} removed from cart!")

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
        bill += f"- {item} x{count}: Rs {st.session_state.products[item] * count}\n"
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



