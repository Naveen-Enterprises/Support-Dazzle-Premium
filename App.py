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
    .warning-box {
        background-color: #ffcccc;
        padding: 1rem;
        border-radius: 10px;
        color: #900;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    h1, h2, h4 { color: #2f80ed; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""<h1 style='text-align: center;'>📦 DAZZLE PREMIUM Order Email Generator</h1>""", unsafe_allow_html=True)

if "reset_clicked" not in st.session_state:
    st.session_state.reset_clicked = False

if st.session_state.reset_clicked:
    for key in ["raw_text"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.reset_clicked = False
    st.rerun()

st.markdown("""<div style='display: flex; gap: 40px;'>""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Paste Shopify Order Export")
        raw_text = st.text_area("Full Order Export Text", height=500, value=st.session_state.get("raw_text", ""))
        generate = st.button("🎯 Generate Email")
        high_risk = st.button("🚨 High-Risk Order Email")

    with col2:
        if generate and raw_text:
            st.session_state.raw_text = raw_text

            name_match = re.search(r"Customer\s*\n(.*)", raw_text)
            if not name_match:
                name_match = re.search(r"Shipping address\s*\n(.*)", raw_text)
            if not name_match:
                name_match = re.search(r"Billing address\s*\n(.*)", raw_text)

            customer_name = name_match.group(1).strip() if name_match else "[Customer Name Not Found]"

            email_match = re.search(r"[\w\.-]+@[\w\.-]+", raw_text)
            phone_match = re.search(r"\+1[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-()]*\d{4}", raw_text)
            order_number_match = re.search(r"dazzlepremium#(\d+)", raw_text)

            email_address = email_match.group(0).strip() if email_match else "[Email Not Found]"
            phone_number = phone_match.group(0).strip() if phone_match else "[Phone Not Found]"
            order_number = order_number_match.group(1).strip() if order_number_match else "[Order # Not Found]"

            lines = [line.strip() for line in raw_text.split('\n') if line.strip() != ""]
            items = []
            i = 0
            while i < len(lines):
                line = lines[i]
                if re.search(r" - [A-Z0-9\-]+$", line) and not any(skip in line for skip in ["SKU", "Discount"]):
                    product_line = line
                    product_name, style_code = product_line.rsplit(" - ", 1)
                    size = "[Size Not Found]"

                    for offset in range(1, 5):
                        if i + offset < len(lines):
                            size_line = lines[i + offset]
                            if re.match(r"^(\d{1,2}[\s/]?[A-Z]{2,3}|[XSML]{1,2})", size_line) and not size_line.startswith("$") and not size_line.startswith("SKU"):
                                size_parts = re.split(r"[ /]", size_line.strip())
                                size = size_parts[0].strip()
                                break

                    items.append((product_name.strip(), style_code.strip(), size))
                i += 1

            order_details = "\n\n".join([
                f"- Item {idx+1}:\n•\u2060  \u2060Product: {p}\n•\u2060  \u2060Style Code: {s}\n•\u2060  \u2060Size: {z}" 
                for idx, (p, s, z) in enumerate(items)
            ])

            subject = f"Final Order Confirmation of dazzlepremium#{order_number}"
            message = f"""Hello {customer_name},

This is DAZZLE PREMIUM Support confirming Order {order_number}

- Please reply YES to confirm just this order only.
- Kindly also reply YES to the SMS sent automatically to your inbox.

Order Details:
{order_details}

For your security, we use two-factor authentication. If this order wasn’t placed by you, text us immediately at 410-381-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""

            missing_info = []
            if "[Customer Name Not Found]" in customer_name:
                missing_info.append("Customer Name")
            if "[Email Not Found]" in email_address:
                missing_info.append("Email Address")
            if "[Phone Not Found]" in phone_number:
                missing_info.append("Phone Number")
            if "[Order # Not Found]" in order_number:
                missing_info.append("Order Number")
            if any("[Size Not Found]" in item[2] for item in items):
                missing_info.append("Item Sizes")

            if missing_info:
                st.markdown(f"<div class='warning-box'>⚠️ Please double-check the following fields: {', '.join(missing_info)}</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div style='background-color:#d4edda;padding:1rem;border-radius:10px;color:#155724;font-weight:bold;margin-bottom:1rem;'>✅ All information looks good. Ready to copy and send.</div>", unsafe_allow_html=True)

            st.markdown(f"<h4>📧 Email Address:</h4><div class='subject-box'>{email_address}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4>📨 Subject:</h4><div class='subject-box'>{subject}</div>", unsafe_allow_html=True)
            st.code(message, language="text")
            st.markdown(f"<h4>📱 Phone Number:</h4><div class='subject-box'>{phone_number}</div>", unsafe_allow_html=True)
            st.button("🔁 Start New Order", on_click=lambda: st.session_state.update({"reset_clicked": True}))

        elif high_risk and raw_text:
            name_match = re.search(r"Customer\s*\n(.*)", raw_text)
            if not name_match:
                name_match = re.search(r"Shipping address\s*\n(.*)", raw_text)
            if not name_match:
                name_match = re.search(r"Billing address\s*\n(.*)", raw_text)
            customer_name = name_match.group(1).strip() if name_match else "[Customer Name Not Found]"

            high_risk_msg = f"""Hello {customer_name},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we’d be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email."""

            st.markdown("<div style='background-color:#fff3cd;padding:1rem;border-radius:10px;color:#856404;font-weight:bold;margin-bottom:1rem;'>⚠️ High-Risk Order Notice</div>", unsafe_allow_html=True)
            st.code(high_risk_msg, language="text")

    if not raw_text:
        st.warning("Please paste the order export before generating the message.")

st.markdown("""</div>""", unsafe_allow_html=True)
