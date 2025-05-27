import streamlit as st
import re

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="wide")
st.markdown("""
<style>
    .main {background-color: #f9f9fb;}
    .stTextInput, .stTextArea {margin-bottom: 1rem;}
    .reportview-container .markdown-text-container { font-size: 1.1rem; }
    .stButton button {background-color: #2f80ed; color: white; font-weight: bold; padding: 0.5rem 1rem; border-radius: 8px;}
    .stButton button:hover {background-color: #1366d6;}
    .stCode {background-color: #f0f2f6; border-radius: 8px;}
    .stAlert {border-radius: 8px;}
    .subject-box {
        background-color: #eef2f8;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: #000000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""<h1 style='text-align: center; color: #2f80ed;'>📦 DAZZLE PREMIUM Order Email Generator</h1>""", unsafe_allow_html=True)

# --- Manage Reset ---
if "reset_clicked" not in st.session_state:
    st.session_state.reset_clicked = False

# --- Handle Reset Safely ---
if st.session_state.reset_clicked:
    for key in ["customer_name", "order_number", "raw_text"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.reset_clicked = False
    st.rerun()

# --- Layout Columns ---
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### Step 1: Enter Customer Info")
    customer_name = st.text_input("Customer Name", value=st.session_state.get("customer_name", ""))
    order_number = st.text_input("Order Number", value=st.session_state.get("order_number", ""))
    raw_text = st.text_area("Paste the order details below exactly as received", height=250, value=st.session_state.get("raw_text", ""))

    if st.button("🎯 Generate Message") and customer_name and order_number and raw_text:
        st.session_state.customer_name = customer_name
        st.session_state.order_number = order_number
        st.session_state.raw_text = raw_text

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

        order_details = "\n\n".join([
            f"- Item {idx+1}:\n•\u2060  \u2060Product: {p}\n•\u2060  \u2060Style Code: {s}\n•\u2060  \u2060Size: {z}" 
            for idx, (p, s, z) in enumerate(items)
        ])

        subject = f"Final Order Confirmation of dazzlepremium#{order_number}"
        message = f"""Hello {customer_name},

This is DAZZLE PREMIUM Support confirming Order {order_number}

- Please reply YES to confirm just this order only.

Order Details:
{order_details}

For your security, we use two-factor authentication. If this order wasn’t placed by you, text us immediately at 301-942-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""

        with col2:
            st.success("✅ Message ready to copy and send")
            st.markdown(f"<h4>📨 Subject:</h4><div class='subject-box'>{subject}</div>", unsafe_allow_html=True)
            st.code(message, language="text")
            st.button("🔁 Start New Order", on_click=lambda: st.session_state.update({"reset_clicked": True}))

# --- Validation ---
if not customer_name or not order_number or not raw_text:
    st.warning("Please fill out all fields before generating the message.")
