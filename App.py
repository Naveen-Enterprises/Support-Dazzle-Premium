import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="centered")
st.title("📦 DAZZLE PREMIUM Order Email Generator")

# --- Simple 4-Field Form ---
st.subheader("🔤 Fill in Order Details")
with st.form("order_form"):
    customer_name = st.text_input("Customer Name")
    order_number = st.text_input("Order Number")
    product_name = st.text_input("Product Name")
    size = st.text_input("Size", value="XL")
    submitted = st.form_submit_button("Generate Message")

if submitted:
    message = f"""Hello {customer_name},

This is DAZZLE PREMIUM Support confirming Order {order_number}

- Please reply YES to confirm just this order only.

Order Details:
• Product: {product_name}
• Style Code:  
• Size: {size}

For your security, we use two-factor authentication. If this order wasn’t placed by you, text us immediately at 301-942-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""

    st.success("✅ Message ready to copy and send")
    st.code(message, language="text")
    st.info("Copy the message above and paste it directly into Gmail, WhatsApp, or SMS. No edits needed.")
