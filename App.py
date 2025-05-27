import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="centered")
st.title("📦 DAZZLE PREMIUM Order Email Generator")

# --- Simple Multi-Item Form ---
st.subheader("🔤 Fill in Order Details")
with st.form("order_form"):
    customer_name = st.text_input("Customer Name")
    order_number = st.text_input("Order Number")
    num_items = st.number_input("How many items in the order?", min_value=1, step=1)
    items = []
    for i in range(int(num_items)):
        st.markdown(f"**Item {i+1}**")
        product_name = st.text_input(f"Product Name {i+1}", key=f"product_{i}")
        style_code = st.text_input(f"Style Code {i+1}", key=f"style_{i}")
        size = st.text_input(f"Size {i+1}", value="XL", key=f"size_{i}")
        items.append((product_name, style_code, size))
    submitted = st.form_submit_button("Generate Message")

if submitted:
    order_details = "\n".join([f"• Product: {p}\n• Style Code: {s}\n• Size: {z}\n" for p, s, z in items])
    message = f"""Hello {customer_name},

This is DAZZLE PREMIUM Support confirming Order {order_number}

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
