
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
    # --- HTML Email Template ---
    html_email = f"""
    <!DOCTYPE html>
    <html>
      <body style='font-family: Arial, sans-serif; background-color: #f8f8f8; padding: 20px;'>
        <div style='background-color: #ffffff; padding: 20px; border-radius: 8px;'>
          <h2 style='color: #111111;'>Hello {customer_name},</h2>
          <p>This is <strong>DAZZLE PREMIUM Support</strong> confirming <strong>Order #{order_number}</strong></p>

          <p><strong>➤ Please reply YES to confirm just this order only.</strong></p>

          <h4>Order Details:</h4>
          <ul>
            <li><strong>Product:</strong> {product_name}</li>
            <li><strong>Style Code:</strong> {style_code}</li>
            <li><strong>Size:</strong> {size}</li>
          </ul>

          <p style='margin-top: 20px;'>
            For your security, we use two-factor authentication. If this order wasn’t placed by you,
            <strong>text us immediately at 301-942-0000</strong> to cancel.
          </p>

          <p><em>Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.</em></p>

          <p>Our US-based team is here Monday–Saturday, 10 AM–6 PM.</p>
          <p style='margin-top: 30px;'>Thank you for choosing <strong>DAZZLE PREMIUM!</strong></p>
        </div>
      </body>
    </html>
    """

    # --- Plain Text Version ---
    plain_text = f"""
Hello {customer_name},
This is DAZZLE PREMIUM Support confirming Order #{order_number}

- Please reply YES to confirm just this order only.

Order Details:
• Product: {product_name}
• Style Code: {style_code}
• Size: {size}

For your security, we use two-factor authentication.
If this order wasn’t placed by you, text us immediately at 301-942-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

Our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!
    """

    st.subheader("✅ Generated HTML Email")
    st.code(html_email, language="html")

    st.subheader("✅ Generated Plain Text Message")
    st.code(plain_text, language="text")
