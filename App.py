import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="wide")
st.title("📦 DAZZLE PREMIUM Order Message Generator")

# --- Input Form ---
st.subheader("🔤 Fill in Order Details")
with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Customer Name")
        order_number = st.text_input("Order Number")
        product_name = st.text_input("Product Name")
        size = st.text_input("Size", value="XL")
    with col2:
        style_code = st.text_input("Style Code")
        email_address = st.text_input("Customer Email")
        phone_number = st.text_input("Customer Phone Number")
    submitted = st.form_submit_button("Generate Messages")

if submitted:
    # --- Email Section ---
    email_subject = f"Final Order Confirmation of dazzlepremium#{order_number}"
    email_body = f"""Hello {customer_name},

This is DAZZLE PREMIUM Support confirming Order {order_number}

- Please reply YES to confirm just this order only.

Order Details:
• Product: {product_name}
• Style Code: {style_code}
• Size: {size}

For your security, we use two-factor authentication. If this order wasn’t placed by you, text us immediately at 410-381-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""

    # --- SMS Section ---
    sms_body = f"Order #{order_number} confirmed for {customer_name}. Product: {product_name}, Size: {size}. If this wasn't you, text us at 410-381-0000."

    # --- Display Sections Side by Side ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### ✉️ Email Message")
        st.markdown(f"**Email Address:** {email_address}")
        st.markdown(f"**Subject:** {email_subject}")
        st.text_area("Body", email_body, height=300)

    with col2:
        st.markdown("### 📱 SMS Message")
        st.markdown(f"**Phone Number:** {phone_number}")
        st.markdown(f"**Order Number:** {order_number}")
        st.text_area("SMS Body", sms_body, height=300)

    st.success("✅ Messages generated and ready to copy")
