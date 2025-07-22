import streamlit as st
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mail - DAZZLE PREMIUM",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    
    .stSelectbox > div > div > div {
        background-color: #f0f2f6;
    }
    
    .missing-info {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .missing-info h4 {
        color: #856404;
        margin: 0 0 0.5rem 0;
    }
    
    .missing-info ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .success-message {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .button-container {
        display: flex;
        gap: 10px;
        margin: 1rem 0;
    }
    
    .copy-button {
        font-size: 0.8rem;
        padding: 0.25rem 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None
if 'email_generated' not in st.session_state:
    st.session_state.email_generated = False

def parse_shopify_data(raw_text):
    """Parse Shopify order data from raw text"""
    data = {
        "customer_name": "[Customer Name Not Found]",
        "email_address": "[Email Not Found]",
        "phone_number": "[Phone Not Found]",
        "order_number": "[Order # Not Found]",
        "items": [],
        "missing_info": []
    }

    if not raw_text.strip():
        return data

    lines = [line.strip() for line in raw_text.split('\n') if line.strip()]

    # Extract customer name
    email_sent_match = re.search(r'Order confirmation email was sent to (.*?) \([\w\.-]+@[\w\.-]+\.[\w\.-]+\)', raw_text, re.IGNORECASE)
    if email_sent_match:
        data["customer_name"] = email_sent_match.group(1).strip()
    else:
        data["missing_info"].append("Customer Name")

    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', raw_text)
    if email_match:
        data["email_address"] = email_match.group(0).strip()
    else:
        data["missing_info"].append("Email Address")

    # Extract phone
    phone_match = re.search(r'(\+1[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4}|\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4})', raw_text)
    if phone_match:
        data["phone_number"] = phone_match.group(0).strip()
    else:
        data["missing_info"].append("Phone Number")

    # Extract order number
    order_match = re.search(r'dazzlepremium#(\d+)', raw_text, re.IGNORECASE)
    if order_match:
        data["order_number"] = order_match.group(1).strip()
    else:
        data["missing_info"].append("Order Number")

    # Extract items (simplified)
    for line in lines:
        if ' - ' in line and 'discount' not in line.lower() and 'total' not in line.lower():
            parts = line.split(' - ')
            if len(parts) >= 2:
                data["items"].append({
                    "product_name": parts[0].strip(),
                    "style_code": parts[1].strip(),
                    "size": "One Size",
                    "quantity": 1
                })

    if not data["items"]:
        data["missing_info"].append("Order Items")

    return data

def generate_standard_email(parsed_data):
    """Generate standard confirmation email"""
    subject = f"Final Order Confirmation of dazzlepremium#{parsed_data['order_number']}"
    
    # Build order details
    order_details = ""
    if len(parsed_data["items"]) > 1:
        for idx, item in enumerate(parsed_data["items"]):
            order_details += f"- Item {idx + 1}:\n"
            order_details += f"•  Product: {item['product_name']}\n"
            order_details += f"•  Style Code: {item['style_code']}\n"
            order_details += f"•  Size: {item['size']}"
            if item["quantity"] > 1:
                order_details += f"\n•  Quantity: {item['quantity']}"
            order_details += "\n\n"
    elif len(parsed_data["items"]) == 1:
        item = parsed_data["items"][0]
        order_details = f"•  Product: {item['product_name']}\n•  Style Code: {item['style_code']}\n•  Size: {item['size']}"
        if item["quantity"] > 1:
            order_details += f"\n•  Quantity: {item['quantity']}"
    else:
        order_details = "No items found."

    message = f"""Hello {parsed_data['customer_name']},

This is DAZZLE PREMIUM Support confirming Order {parsed_data['order_number']}

- Please reply YES to confirm just this order only.
- Kindly also reply YES to the SMS sent automatically to your inbox.

Order Details:
{order_details}

For your security, we use two-factor authentication. If this order wasn't placed by you, text us immediately at 410-381-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""

    return parsed_data["email_address"], subject, message

def generate_high_risk_email(parsed_data):
    """Generate high-risk cancellation email"""
    subject = "Important: Your DAZZLE PREMIUM Order - Action Required"
    message = f"""Hello {parsed_data['customer_name']},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we'd be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email.

Thank you,
DAZZLE PREMIUM Support"""

    return parsed_data["email_address"], subject, message

def generate_return_email(parsed_data):
    """Generate return instructions email"""
    subject = "DAZZLE PREMIUM: Your Return Request Instructions"
    message = f"""Dear {parsed_data['customer_name']},

Thank you for reaching out to us regarding your return request. To ensure a smooth and successful return process, please carefully follow the steps below:

1. Go to your local post office or any shipping carrier (USPS, FedEx, UPS, DHL).

2. Create and pay for the return shipping label.
(Please note: You are responsible for the return shipping cost.)

3. Ship the item to the following address:

Dazzle Premium 
3500 East-West Highway 
Suite 1032 
Hyattsville, MD 20782 
+1 (301) 942-0000 

4. Email us the tracking number after you ship the package by replying to this email.

Once we receive the returned item in its original condition with the tags intact and complete our inspection, we will process your refund.

If you have any questions, feel free to reply to this email."""

    return parsed_data["email_address"], subject, message

# Main app layout
st.title("📧 Mail - DAZZLE PREMIUM")
st.markdown("### Premium Email Generator")

# Current date and time
current_time = datetime.now()
st.info(f"📅 {current_time.strftime('%A, %B %d, %Y')} | 🕒 {current_time.strftime('%I:%M:%S %p')}")

# Create two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### 📋 Order Data Input")
    
    # Text area for order data
    order_data = st.text_area(
        "Paste Shopify order export here:",
        height=300,
        placeholder="Paste your Shopify order export here..."
    )
    
    # Parse button
    if st.button("🔍 Parse Order Data", type="primary"):
        if order_data.strip():
            st.session_state.parsed_data = parse_shopify_data(order_data)
            st.session_state.email_generated = False
        else:
            st.warning("Please paste order data first.")
    
    # Display missing information if any
    if st.session_state.parsed_data and st.session_state.parsed_data.get("missing_info"):
        st.markdown("""
        <div class="missing-info">
            <h4>⚠️ Missing Information</h4>
            <ul>
        """, unsafe_allow_html=True)
        for item in st.session_state.parsed_data["missing_info"]:
            st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)
    
    # Email generation buttons
    st.markdown("#### ✨ Generate Email")
    
    col1a, col1b, col1c = st.columns(3)
    
    with col1a:
        if st.button("✨ Standard", use_container_width=True):
            if st.session_state.parsed_data:
                st.session_state.email_data = generate_standard_email(st.session_state.parsed_data)
                st.session_state.email_generated = True
            else:
                st.warning("Parse order data first!")
    
    with col1b:
        if st.button("🚨 High Risk", use_container_width=True):
            if st.session_state.parsed_data:
                st.session_state.email_data = generate_high_risk_email(st.session_state.parsed_data)
                st.session_state.email_generated = True
            else:
                st.warning("Parse order data first!")
    
    with col1c:
        if st.button("↩️ Return", use_container_width=True):
            if st.session_state.parsed_data:
                st.session_state.email_data = generate_return_email(st.session_state.parsed_data)
                st.session_state.email_generated = True
            else:
                st.warning("Parse order data first!")

with col2:
    st.markdown("#### ✉️ Compose Email")
    
    if st.session_state.email_generated and 'email_data' in st.session_state:
        email_to, email_subject, email_body = st.session_state.email_data
        
        # Success indicator
        st.markdown("""
        <div class="success-message">
            <strong>✅ Email Generated Successfully!</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Email fields with built-in copy functionality
        st.subheader("📧 To:")
        st.code(email_to, language=None)
        
        st.subheader("📝 Subject:")
        st.code(email_subject, language=None)
        
        st.subheader("💬 Message:")
        st.code(email_body, language=None)
    
    else:
        st.info("👆 Parse order data and select an email type to generate the email content.")
        
        # Placeholder fields
        st.text_input("To:", placeholder="Recipient email will appear here", disabled=True)
        st.text_input("Subject:", placeholder="Email subject will appear here", disabled=True)
        st.text_area("Message:", placeholder="Email message will appear here...", height=400, disabled=True)

# Footer
st.markdown("---")
st.markdown("**DAZZLE PREMIUM** - Premium Email Management System")
