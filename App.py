import streamlit as st
import re

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="centered")
st.title("📦 DAZZLE PREMIUM Order Email Generator")

# --- Manage Navigation State ---
if "step" not in st.session_state:
    st.session_state.step = 1

# --- Screen 1: Ask for order number and name ---
if st.session_state.step == 1:
    st.subheader("Step 1: Enter Customer Info")
    customer_name = st.text_input("Customer Name")
    order_number = st.text_input("Order Number")
    if st.button("Next") and customer_name and order_number:
        st.session_state.customer_name = customer_name
        st.session_state.order_number = order_number
        st.session_state.step = 2

# --- Screen 2: Paste Raw Item Info ---
elif st.session_state.step == 2:
    st.subheader("Step 2: Paste Raw Item Info")
    raw_text = st.text_area("Paste the order details below exactly as received")
    if st.button("Next") and raw_text:
        st.session_state.raw_text = raw_text
        st.session_state.step = 3

# --- Screen 3: Parse and Generate Message ---
elif st.session_state.step == 3:
    st.subheader("Step 3: Generated Order Message")

    raw_text = st.session_state.raw_text
    # Basic parsing logic to extract products
    lines = [line.strip() for line in raw_text.split('\n') if line.strip() != ""]
    items = []
    i = 0
    while i < len(lines):
        if '-' in lines[i] and not lines[i].startswith("SKU"):
            product_line = lines[i]
            size_line = lines[i+1] if i+1 < len(lines) else ""
            sku_line = lines[i+2] if i+2 < len(lines) and lines[i+2].startswith("SKU") else ""

            product_name = product_line.split('-')[0].strip()
            style_code = product_line.split('-')[-1].strip()
            size = size_line.split('/')[0].strip() if '/' in size_line else size_line.strip()

            items.append((product_name, style_code, size))
            i += 4  # Skip to next item block
        else:
            i += 1

    if st.button("Generate Message"):
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
