import streamlit as st
import pyperclip

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="centered")
st.title("📦 DAZZLE PREMIUM Order Email Generator")

# --- Input Form ---
st.subheader("Enter Order Details")
with st.form("order_form"):
    customer_name = st.text_input("Customer Name", value="D'Juan Neal")
    order_number = st.text_input("Order Number", value="1625")
    product_name = st.text_input("Product Name", value="Reverse Terry Half Zip (Yellow)")
    style_code = st.text_input("Style Code", value="300408")
    size = st.text_input("Size", value="XL")
    submitted = st.form_submit_button("Generate Email")

if submitted:
    # --- HTML Email Template ---
    html_email = f"""
Hello {customer_name},

This is DAZZLE PREMIUM Support confirming Order #{order_number}

➤ Please reply YES to confirm just this order only.

Order Details:
- Product: {product_name}
- Style Code: {style_code}
- Size: {size}

For your security, we use two-factor authentication. If this order wasn’t placed by you,
text us immediately at 301-942-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

Our US-based team is here Monday–Saturday, 10 AM–6 PM.

Thank you for choosing DAZZLE PREMIUM!
    """

    st.success("✅ Email is ready to send!")

    st.subheader("📤 One-Click Copy")
    st.text_area("✉️ Copy & Paste This Message into Gmail or SMS", html_email, height=300)

    if st.button("📋 Copy to Clipboard"):
        try:
            pyperclip.copy(html_email)
            st.success("Copied to clipboard!")
        except:
            st.warning("Clipboard copy not supported in this browser. Please copy manually.")

    st.info("✅ Just paste this message directly into Gmail or SMS. No formatting tricks needed.")
