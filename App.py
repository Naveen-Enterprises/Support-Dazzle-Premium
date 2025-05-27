import streamlit as st

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
    # --- Message Template ---
    final_message = f"""
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

    st.subheader("📋 Copy & Paste Message")
    st.code(final_message, language="text")
    st.info("Right-click the box above and select 'Copy' or press Ctrl+C (Cmd+C on Mac). Then paste into Gmail or SMS.")
