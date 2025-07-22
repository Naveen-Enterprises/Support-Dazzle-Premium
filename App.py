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

            # Extract Customer Name
            name_match = re.search(r"Customer\s*\n(.*)", raw_text)
            if not name_match:
                name_match = re.search(r"Shipping address\s*\n(.*)", raw_text)
            if not name_match:
                name_match = re.search(r"Billing address\s*\n(.*)", raw_text)
            customer_name = name_match.group(1).strip() if name_match else "[Customer Name Not Found]"

            # Extract Email, Phone, Order Number
            email_match = re.search(r"[\w\.-]+@[\w\.-]+", raw_text)
            phone_match = re.search(r"\+1[\s\-()]*\d{3}[\s\-()]*\d{3}[\s\-()]*\d{4}", raw_text)
            order_number_match = re.search(r"dazzlepremium#(\d+)", raw_text)

            email_address = email_match.group(0).strip() if email_match else "[Email Not Found]"
            phone_number = phone_match.group(0).strip() if phone_match else "[Phone Not Found]"
            order_number = order_number_match.group(1).strip() if order_number_match else "[Order # Not Found]"

            # Parse Order Items
            lines = [line.strip() for line in raw_text.split('\n') if line.strip() != ""]
            items = []
            i = 0
            while i < len(lines):
                line = lines[i]
                # Identify product lines by their format ending with " - SKU"
                if re.search(r" - [A-Z0-9\-]+$", line) and not any(skip in line for skip in ["SKU", "Discount"]):
                    product_line = line
                    product_name, style_code = product_line.rsplit(" - ", 1)
                    size = "[Size Not Found]"

                    # Look for size in subsequent lines
                    for offset in range(1, 5): # Check up to 4 lines after the product line
                        if i + offset < len(lines):
                            size_line = lines[i + offset].strip()
                            # Attempt to match numerical size (e.g., "32" from "32 / DK.BLU")
                            size_match_num = re.match(r"^(\d{1,2})", size_line)
                            if size_match_num:
                                size = size_match_num.group(1).strip()
                                break
                            # Attempt to match common letter sizes (e.g., "XS", "M")
                            size_match_letters = re.match(r"^[XSML]{1,2}[XS]?", size_line)
                            if size_match_letters:
                                size = size_match_letters.group(0).strip()
                                break
                            # Fallback for simple single-word sizes not caught above, ensuring it's not a price/SKU
                            if not size_line.startswith("$") and not size_line.startswith("SKU") and len(size_line.split()) == 1 and len(size_line) > 0 and len(size_line) < 10:
                                size = size_line
                                break
                
                    items.append((product_name.strip(), style_code.strip(), size))
                i += 1

            # Construct Order Details string based on item count
            order_details_list = []
            for idx, (p, s, z) in enumerate(items):
                # Conditional item count and style code
                item_prefix = ""
                if len(items) > 1:
                    item_prefix = f"- Item {idx+1}:\n"
                
                # Using regular spaces for bullet points
                item_detail = f"{item_prefix}• Product: {p}\n• Size: {z}"
                
                # Only include Style Code if there are multiple items
                if len(items) > 1:
                    item_detail += f"\n• Style Code: {s}"
                order_details_list.append(item_detail)

            order_details = "\n\n".join(order_details_list) # Use \n\n for spacing between items

            # Construct Email Subject and Message
            subject = f"Final Order Confirmation of dazzlepremium#{order_number}"
            
            # Building the message line by line to explicitly control newlines and spacing
            message_lines = [
                f"Hello {customer_name},",
                "", # Empty line for spacing
                f"This is DAZZLE PREMIUM Support confirming Order {order_number}",
                "", # Empty line for spacing
                "<b>- Please reply YES to confirm just this order only.<br>",
                "- Kindly also reply YES to the SMS sent automatically to your inbox.</b>",
                "", # Empty line for spacing
                "Order Details:",
                order_details, # This already contains its own internal newlines
                "", # Empty line for spacing
                "For your security, we use two-factor authentication. If this order wasn’t placed by you, text us immediately at 410-381-0000 to cancel.",
                "", # Empty line for spacing
                "<b>Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.</b>",
                "", # Empty line for spacing
                "If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.",
                "Thank you for choosing DAZZLE PREMIUM!"
            ]
            message = "\n".join(message_lines)

            # Check for missing information and display warnings
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

            # Display generated email components
            st.markdown(f"<h4>📧 Email Address:</h4><div class='subject-box'>{email_address}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4>📨 Subject:</h4><div class='subject-box'>{subject}</div>", unsafe_allow_html=True)
            
            st.markdown("<h4>📋 Formatted Email Preview:</h4>", unsafe_allow_html=True)
            # Display the formatted email using st.markdown for visual preview
            st.markdown(message, unsafe_allow_html=True) 

            st.markdown("<h4>📋 Copy Email Body (for pasting):</h4>", unsafe_allow_html=True)
            # Use st.text_area for the message to allow easy copying by the user
            st.text_area("Email Body", value=message, height=350, key="generated_email_body")
            st.markdown("<p style='font-size:0.9rem; color:#555;'>👆 Copy the text above and paste it into your email client. <b>Ensure your email client is set to compose in HTML/Rich Text mode for correct formatting.</b></p>", unsafe_allow_html=True)

            st.markdown(f"<h4>📱 Phone Number:</h4><div class='subject-box'>{phone_number}</div>", unsafe_allow_html=True)
            st.button("🔁 Start New Order", on_click=lambda: st.session_state.update({"reset_clicked": True}))

        elif high_risk and raw_text:
            # Logic for High-Risk Order Email
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
            
            st.markdown("<h4>📋 Formatted Email Preview:</h4>", unsafe_allow_html=True)
            st.markdown(high_risk_msg, unsafe_allow_html=True)

            st.markdown("<h4>📋 Copy Email Body (for pasting):</h4>", unsafe_allow_html=True)
            st.text_area("High-Risk Email Body", value=high_risk_msg, height=350, key="high_risk_email_body")
            st.markdown("<p style='font-size:0.9rem; color:#555;'>👆 Copy the text above and paste it into your email client. <b>Ensure your email client is set to compose in HTML/Rich Text mode for correct formatting.</b></p>", unsafe_allow_html=True)
            st.button("🔁 Start New Order", on_click=lambda: st.session_state.update({"reset_clicked": True}))

    # Display warning if raw_text is empty and generate/high_risk buttons are clicked
    if (generate or high_risk) and not raw_text:
        st.warning("Please paste the order export before generating the message.")

st.markdown("""</div>""", unsafe_allow_html=True)
```
