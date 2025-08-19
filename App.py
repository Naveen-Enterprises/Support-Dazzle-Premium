import streamlit as st
import re
import json # Import the json module

# --- Page Configuration ---
st.set_page_config(page_title="DAZZLE PREMIUM Order Email Generator", layout="wide", initial_sidebar_state="collapsed")

# --- Custom CSS Styling (Inspired by Material Design & Apple Aesthetics) ---
# Using Google Fonts (Inter for body, Montserrat for headings)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@700&display=swap" rel="stylesheet">
<style>
    /* ...existing CSS... */
</style>
""", unsafe_allow_html=True)

# --- JavaScript for Copy to Clipboard Functionality ---
st.markdown("""
<script>
function copyToClipboard(text, elementId) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand('copy');
        const element = document.getElementById(elementId);
        if (element) {
            element.innerText = 'Copied!';
            setTimeout(() => { element.innerText = 'Copy'; }, 1500);
        }
    } catch (err) {
        console.error('Failed to copy text: ', err);
    }
    document.body.removeChild(textarea);
}
</script>
""", unsafe_allow_html=True)

# --- Initialize Session State ---
if "current_step" not in st.session_state:
    st.session_state.current_step = "input"
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = {}
if "generated_email_body" not in st.session_state:
    st.session_state.generated_email_body = ""
if "generated_subject" not in st.session_state:
    st.session_state.generated_subject = ""
if "missing_info_flags" not in st.session_state:
    st.session_state.missing_info_flags = []

# --- Helper Functions ---
def parse_shopify_export(raw_text_input):
    # ...existing code...
    # (No changes needed here)
    # ...existing code...
    return data

def generate_standard_email(parsed_data):
    # ...existing code...
    return subject, message

def generate_high_risk_email(parsed_data):
    # ...existing code...
    return subject, message

def generate_return_email(parsed_data):
    # ...existing code...
    return subject, message

def generate_medium_risk_email(parsed_data):
    """Generates the medium-risk order verification email."""
    customer_name = parsed_data.get("customer_name", "[Customer Name Not Found]")
    order_number = parsed_data.get("order_number", "[Order # Not Found]")
    items = parsed_data.get("items", [])

    order_details_list = []
    for item in items:
        item_detail = (
            f"• Product: {item.get('product_name', 'N/A')}\n"
            f"• Style Code: {item.get('style_code', 'N/A')}\n"
            f"• Size: {item.get('size', 'Size Not Found')}"
        )
        order_details_list.append(item_detail)
    order_details = "\n".join(order_details_list) if order_details_list else "No items found."

    subject = f"Verification Required for dazzlepremium#{order_number}"
    message = f"""Hello {customer_name},

Thank you for shopping with DAZZLE PREMIUM. Our system has flagged your recent order (#{order_number}) for additional verification. For your security and to prevent fraudulent activity, we are unable to ship this order until it has been manually reviewed and confirmed.

Order Details:
{order_details}

To complete verification, please reply to this email with:
- Your Order Number
- A valid photo ID (you may cover sensitive information, but your name must be visible)
- A picture of the payment card used (you may cover all digits except the last 4)

Once we receive this information, our fraud prevention team will promptly review it and proceed with shipping.

For your security: If you did not place this order, please text us immediately at 410-381-0000 so we can cancel and secure your account.

Note: Any order confirmed after 3:00 PM will be scheduled for the next business day.

If you have any questions, our US-based team is available Monday–Saturday, 10 AM–6 PM.

We truly value your safety and appreciate your cooperation.

Thank you for choosing DAZZLE PREMIUM!
"""
    return subject, message

def reset_app_state():
    st.session_state.current_step = "input"
    st.session_state.raw_text = ""
    st.session_state.parsed_data = {}
    st.session_state.generated_email_body = ""
    st.session_state.generated_subject = ""
    st.session_state.missing_info_flags = []
    st.rerun()

# --- Main Application Logic ---
st.markdown("""<h1 style='text-align: center;'>📦 DAZZLE PREMIUM Order Email Generator</h1>""", unsafe_allow_html=True)

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Paste Shopify Order Export")
    st.markdown("""
        <div class="info-card">
            <span style="font-size: 1.2rem;">📄</span>
            Paste the full text from your Shopify order export summary below.
            We'll automatically extract all the necessary details.
        </div>
    """, unsafe_allow_html=True)

    raw_text_input = st.text_area(
        "Full Order Export Text",
        height=400,
        value=st.session_state.raw_text,
        placeholder="Paste your Shopify order details here...",
        key="raw_text_input_main"
    )

    col_buttons_input = st.columns(4) # Changed to 4 columns for 4 buttons
    with col_buttons_input[0]:
        if st.button("✨ Generate Order Email", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                st.session_state.parsed_data = parse_shopify_export(raw_text_input)
                st.session_state.missing_info_flags = st.session_state.parsed_data["missing_info"]
                subject, message = generate_standard_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_standard"
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate an email.")
    with col_buttons_input[1]:
        if st.button("🚨 High-Risk Email", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                st.session_state.parsed_data = parse_shopify_export(raw_text_input)
                st.session_state.missing_info_flags = st.session_state.parsed_data["missing_info"]
                subject, message = generate_high_risk_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_high_risk"
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate a high-risk email.")
    with col_buttons_input[2]:
        if st.button("↩️ Return Email Template", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                st.session_state.parsed_data = parse_shopify_export(raw_text_input)
                st.session_state.missing_info_flags = st.session_state.parsed_data["missing_info"]
                subject, message = generate_return_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_return"
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate a return email.")
    with col_buttons_input[3]:
        if st.button("🟡 Medium-Risk Email", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                st.session_state.parsed_data = parse_shopify_export(raw_text_input)
                st.session_state.missing_info_flags = st.session_state.parsed_data["missing_info"]
                subject, message = generate_medium_risk_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_medium_risk"
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate a medium-risk email.")

    st.button("🔄 Reset All", on_click=reset_app_state, use_container_width=True)

with col_right:
    st.subheader("2. Your Generated Email")
    if st.session_state.generated_email_body:
        if st.session_state.missing_info_flags and st.session_state.current_step == "generate_standard":
            missing_text = ", ".join(st.session_state.missing_info_flags)
            st.markdown(f"""
                <div class="warning-card">
                    <span style="font-size: 1.2rem;">⚠️</span>
                    <strong>Missing Information:</strong> Could not automatically extract: {missing_text}.
                    Please verify the generated email and manually add/correct these details.
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.current_step == "generate_high_risk":
            st.markdown("""
                <div class="warning-card">
                    <span style="font-size: 1.2rem;">🚨</span>
                    This is the email for high-risk order cancellations. Please review carefully before sending.
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.current_step == "generate_return":
            st.markdown("""
                <div class="info-card">
                    <span style="font-size: 1.2rem;">↩️</span>
                    This is the return mail template. Ensure the customer name is correct.
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.current_step == "generate_medium_risk":
            st.markdown("""
                <div class="warning-card">
                    <span style="font-size: 1.2rem;">🟡</span>
                    This is the email for medium-risk order verification. Please review before sending.
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="success-card">
                    <span style="font-size: 1.2rem;">✅</span>
                    Email generated successfully! Ready to copy and send.
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<h4>📧 Recipient Email:</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="data-display-box">
                <span>{st.session_state.parsed_data.get('email_address', 'N/A')}</span>
                <button class="copy-button" id="copyEmailBtn" onclick="copyToClipboard(
                    '{st.session_state.parsed_data.get('email_address', 'N/A').replace("'", "\\'")}', 'copyEmailBtn'
                )">Copy</button>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<h4>📨 Subject:</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class="data-display-box">
                <span>{st.session_state.generated_subject}</span>
                <button class="copy-button" id="copySubjectBtn" onclick="copyToClipboard(
                    '{st.session_state.generated_subject.replace("'", "\\'")}', 'copySubjectBtn'
                )">Copy</button>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<h4>📝 Email Body:</h4>", unsafe_allow_html=True)
        st.code(st.session_state.generated_email_body, language="text")
        
        js_safe_email_body = json.dumps(st.session_state.generated_email_body)
        st.markdown(f"""
            <div style="text-align: right; margin-top: -0.8rem; margin-bottom: 0.8rem;">
                <button class="copy-button" id="copyBodyBtn" onclick="copyToClipboard(
                    {js_safe_email_body}, 'copyBodyBtn'
                )">Copy Email Body</button>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.current_step == "generate_standard":
            st.markdown(f"""
                <div class="extracted-data-card">
                    <h3><span style="font-size: 1.2rem;">🔍</span> Additional Order Details</h3>
                    <div class="field-row">
                        <span class="field-label">Customer Name:</span>
                        <span class="field-value-display">{st.session_state.parsed_data.get('customer_name', '[Not Found]')}</span>
                    </div>
                    <div class="field-row">
                        <span class="field-label">Order Number:</span>
                        <span class="field-value-display">{st.session_state.parsed_data.get('order_number', '[Not Found]')}</span>
                    </div>
                    <div class="field-row">
                        <span class="field-label">Phone:</span>
                        <span class="field-value-display">{st.session_state.parsed_data.get('phone_number', '[Not Found]')}</span>
                    </div>
                    <h4>Order Items:</h4>
            """, unsafe_allow_html=True)

            if st.session_state.parsed_data.get("items"):
                for item in st.session_state.parsed_data["items"]:
                    st.markdown(f"""
                        <div class="order-item">
                            <div class="item-detail"><span class="label">Product:</span> <span class="value">{item.get('product_name', 'N/A')}</span></div>
                            <div class="item-detail"><span class="label">Style Code:</span> <span class="value">{item.get('style_code', 'N/A')}</span></div>
                            <div class="item-detail"><span class="label">Size:</span> <span class="value">{item.get('size', 'Size Not Found')}</span></div>
                            <div class="item-detail"><span class="label">Quantity:</span> <span class="value">{item.get('quantity', 1)}</span></div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""<div class="info-card">No items extracted.</div>""", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        st.button("🔁 Start New Order", on_click=reset_app_state, use_container_width=True)
    else:
        st.markdown("""
            <div class="info-card" style="min-height: 500px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                <span style="font-size: 2.2rem; margin-bottom: 0.7rem;">✨</span>
                <p style="font-size: 1rem; font-weight: 600;">Your generated email will appear here.</p>
                <p style="color: var(--text-medium); font-size: 0.85rem;">Paste your order details on the left and click 'Generate Email' to see the magic!</p>
            </div>
        """, unsafe_allow_html=True)
