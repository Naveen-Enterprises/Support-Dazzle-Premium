import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="centered")
st.title("📦 DAZZLE PREMIUM Order Email Generator")

# --- Manage Navigation State ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "items" not in st.session_state:
    st.session_state.items = {}

# --- Screen 1: Ask for order number and name ---
if st.session_state.step == 1:
    st.subheader("Step 1: Enter Customer Info")
    customer_name = st.text_input("Customer Name")
    order_number = st.text_input("Order Number")
    if st.button("Next") and customer_name and order_number:
        st.session_state.customer_name = customer_name
        st.session_state.order_number = order_number
        st.session_state.step = 2

# --- Screen 2: Ask number of items ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Number of Items")
    num_items = st.number_input("How many items in the order?", min_value=1, step=1)
    if st.button("Next"):
        st.session_state.num_items = num_items
        st.session_state.step = 3

# --- Screen 3: Enter details and generate message ---
elif st.session_state.step == 3:
    st.subheader("Step 3: Enter Item Details")
    for i in range(int(st.session_state.num_items)):
        st.markdown(f"**Item {i+1}**")
        if f"product_{i}" not in st.session_state:
            st.session_state[f"product_{i}"] = ""
        if f"style_{i}" not in st.session_state:
            st.session_state[f"style_{i}"] = ""
        if f"size_{i}" not in st.session_state:
            st.session_state[f"size_{i}"] = "XL"

        st.session_state[f"product_{i}"] = st.text_input(f"Product Name {i+1}", value=st.session_state[f"product_{i}"], key=f"product_{i}")
        st.session_state[f"style_{i}"] = st.text_input(f"Style Code {i+1}", value=st.session_state[f"style_{i}"], key=f"style_{i}")
        st.session_state[f"size_{i}"] = st.text_input(f"Size {i+1}", value=st.session_state[f"size_{i}"], key=f"size_{i}")

    if st.button("Generate Message"):
        items = [(st.session_state[f"product_{i}"], st.session_state[f"style_{i}"], st.session_state[f"size_{i}"]) for i in range(int(st.session_state.num_items))]
        order_details = "\n".join([f"• Product: {p}\n• Style Code: {s}\n• Size: {z}" for p, s, z in items])
        message = f"""Hello {st.session_state.customer_name},

This is DAZZLE PREMIUM Support confirming Order {st.session_state.order_number}

- Please reply YES to confirm just this order only.

Order Details:
{order_details}

For your security, we use two-factor authentication. If this order wasn’t placed by you, text us immediately at 301-942-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""

        st.success("✅ Message ready to copy and send")
        st.code(message, language="text")
        st.info("Copy the message above and paste it directly into Gmail, WhatsApp, or SMS. No edits needed.")
