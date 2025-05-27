import streamlit as st
import re

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="wide")
st.markdown("""
<style>
    body { font-family: 'Segoe UI', sans-serif; font-size: 16px; }
    .main {background-color: #ffffff; padding: 2rem;}
    .stTextInput > div > input,
    .stTextArea > div > textarea {
        padding: 0.75rem;
        font-size: 1rem;
        border-radius: 10px;
        border: 1px solid #ccc;
    }
    .stButton button {
        background-color: #2f80ed;
        color: white;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #1366d6;
    }
    .stCode {
        background-color: #f7f8fa;
        border-radius: 10px;
        padding: 1rem;
        font-size: 0.95rem;
    }
    .subject-box {
        background-color: #eef2f8;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #1a1a1a;
        font-weight: 500;
        font-size: 1rem;
    }
    h1, h2, h4 { color: #2f80ed; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""<h1 style='text-align: center;'>📦 DAZZLE PREMIUM Order Email Generator</h1>""", unsafe_allow_html=True)

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
st.markdown("""<div style='display: flex; gap: 40px;'>""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Enter Customer Info")
        customer_name = st.text_input("Customer Name", value=st.session_state.get("customer_name", ""))
        order_number = st.text_input("Order Number", value=st.session_state.get("order_number", ""))
        raw_text = st.text_area("Paste Order Details", height=300, value=st.session_state.get("raw_text", ""))
        generate = st.button("🎯 Generate Message")

    with col2:
        if generate and customer_name and order_number and raw_text:
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

            st.success("✅ Message ready to copy and send")
            st.markdown(f"<h4>📨 Subject:</h4><div class='subject-box'>{subject}</div>", unsafe_allow_html=True)
            st.code(message, language="text")
            st.button("🔁 Start New Order", on_click=lambda: st.session_state.update({"reset_clicked": True}))

    if not customer_name or not order_number or not raw_text:
        st.warning("Please fill out all fields before generating the message.")

st.markdown("""</div>""", unsafe_allow_html=True)
