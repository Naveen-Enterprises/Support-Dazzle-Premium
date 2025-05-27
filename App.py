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
    lines = [line.strip() for line in raw_text.split('\n') if line.strip() != ""]
    items = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if '-' in line and not line.startswith("SKU") and not "Discount" in line:
            product_line = line
            next_lines = lines[i+1:i+4] if i+4 <= len(lines) else lines[i+1:]

            product_name = product_line.split('-')[0].strip()
            style_code = product_line.split('-')[-1].strip()
            size = ""
            for l in next_lines:
                if '/' in l and not l.startswith("$"):
                    size = l.split('/')[0].strip()
                    break

            items.append((product_name, style_code, size))
            i += len(next_lines) + 1
        else:
            i += 1

    if st.button("Generate Message"):
        order_details = "\n\n".join([
            f"- Item {idx+1}:\n•\u2060  \u2060Product: {p}\n•\u2060  \u2060Style Code: {s}\n•\u2060  \u2060Size: {z}" 
            for idx, (p, s, z) in enumerate(items)
        ])

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
