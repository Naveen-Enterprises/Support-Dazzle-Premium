import streamlit as st
from datetime import datetime
import re

# --- Helper Functions (Python equivalents of your JavaScript logic) ---

def parse_shopify_data(raw_text):
    """
    Parses raw Shopify order data to extract customer information and order details.
    """
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
    email_sent_match = re.search(r"Order confirmation email was sent to (.*?) \([\w\.-]+@[\w\.-]+\.[\w\.-]+\)", raw_text, re.IGNORECASE)
    if email_sent_match:
        data["customer_name"] = email_sent_match.group(1).strip()
    else:
        data["missing_info"].append("Customer Name")

    # Extract email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.[\w\.-]+", raw_text)
    if email_match:
        data["email_address"] = email_match.group(0).strip()
    else:
        data["missing_info"].append("Email Address")

    # Extract phone
    phone_match = re.search(r"(\+1[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4}|\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4})", raw_text)
    if phone_match:
        data["phone_number"] = phone_match.group(0).strip()
    else:
        data["missing_info"].append("Phone Number")

    # Extract order number
    order_match = re.search(r"dazzlepremium#(\d+)", raw_text, re.IGNORECASE)
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
                    "size": "One Size",  # Default as per JS
                    "quantity": 1        # Default as per JS
                })

    if not data["items"]:
        data["missing_info"].append("Order Items")

    return data

def get_order_details_string(items):
    """Formats the order items into a readable string."""
    if len(items) > 1:
        details = []
        for idx, item in enumerate(items):
            item_detail = f"- Item {idx + 1}:\n"
            item_detail += f"•  Product: {item['product_name']}\n"
            item_detail += f"•  Style Code: {item['style_code']}\n"
            item_detail += f"•  Size: {item['size']}"
            if item['quantity'] > 1:
                item_detail += f"\n•  Quantity: {item['quantity']}"
            details.append(item_detail)
        return "\n\n".join(details)
    elif len(items) == 1:
        item = items[0]
        details = f"•  Product: {item['product_name']}\n•  Style Code: {item['style_code']}\n•  Size: {item['size']}"
        if item['quantity'] > 1:
            details += f"\n•  Quantity: {item['quantity']}"
        return details
    else:
        return "No items found."

# --- Streamlit UI ---

st.set_page_config(layout="wide", page_title="Mail - DAZZLE PREMIUM")

# Custom CSS for styling (adapted from your HTML/CSS)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', system-ui, sans-serif;
            color: #1d1d1f;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            background: linear-gradient(135deg, #e0eafc, #cfdef3); /* Light blue gradient background */
        }
        
        .stApp {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            gap: 20px;
            display: flex; /* For responsive layout in columns */
            flex-direction: column; /* Default for small screens */
            align-items: stretch;
            min-height: 100vh;
        }

        .stApp > header {
            display: none; /* Hide Streamlit's default header */
        }

        .stApp > div:first-child {
            padding-top: 0px;
        }

        .stApp > div:nth-child(2) { /* This targets the main content area */
            display: flex;
            flex-direction: column; /* Default to column for smaller screens */
            gap: 20px;
        }

        .sidebar-panel {
            flex: 1;
            max-width: 320px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            flex-direction: column;
            min-height: calc(100vh - 40px); /* Adjust for padding */
        }

        .main-content-panel {
            flex: 2;
            background: rgba(255, 255, 255, 0.98);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            display: flex;
            flex-direction: column;
            min-height: calc(100vh - 40px); /* Adjust for padding */
        }

        .app-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #007AFF, #5856D6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            text-align: center;
        }

        .app-subtitle {
            color: #86868b;
            font-size: 1.1rem;
            font-weight: 500;
            text-align: center;
            margin-bottom: 40px;
        }

        .section-title {
            font-size: 1.4rem;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .section-icon {
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #007AFF, #5856D6);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 0.9rem;
        }

        .date-display {
            background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
        }

        .current-date {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1d1d1f;
            margin-bottom: 5px;
        }

        .current-time {
            font-size: 1rem;
            color: #86868b;
            font-weight: 500;
        }

        .missing-info {
            background: linear-gradient(135deg, #FFE4B5, #FFEAA7);
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 30px;
            border-left: 4px solid #FF6B35;
        }

        .missing-info h3 {
            color: #D63031;
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .missing-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .missing-list li {
            color: #2D3436;
            font-size: 0.95rem;
            margin-bottom: 5px;
            padding-left: 20px;
            position: relative;
        }

        .missing-list li:before {
            content: "•";
            color: #FF6B35;
            font-weight: bold;
            position: absolute;
            left: 0;
        }

        .compose-header {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 25px;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-label {
            display: block;
            font-size: 0.95rem;
            font-weight: 600;
            color: #1d1d1f;
            margin-bottom: 8px;
        }

        .stTextInput > div > div > input, .stTextArea > div > div > textarea {
            width: 100%;
            padding: 15px 18px;
            border: 2px solid #e5e5e7;
            border-radius: 12px;
            font-size: 1rem;
            font-family: inherit;
            background: white;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            line-height: 1.6; /* For textarea */
        }
        
        .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
            outline: none;
            border-color: #007AFF;
            box-shadow: 0 0 0 4px rgba(0, 122, 255, 0.1);
            transform: translateY(-1px);
        }

        .stTextInput > label, .stTextArea > label {
            display: none; /* Hide default Streamlit labels, we use custom ones */
        }

        div.stButton > button {
            flex: 1;
            padding: 16px 24px;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
            width: 100%; /* Make buttons full width */
            margin-bottom: 15px; /* Spacing between buttons */
        }

        div.stButton > button:before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            transition: left 0.5s;
        }

        div.stButton > button:hover:before {
            left: 100%;
        }

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
        }

        div.stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        /* Button specific colors */
        div.stButton > button:nth-of-type(1) { /* Standard button */
            background: linear-gradient(135deg, #007AFF, #5856D6);
            color: white;
        }
        div.stButton > button:nth-of-type(2) { /* High Risk button */
            background: linear-gradient(135deg, #FF6B35, #FF8E53);
            color: white;
        }
        div.stButton > button:nth-of-type(3) { /* Return button */
            background: linear-gradient(135deg, #00D2FF, #3A7BD5);
            color: white;
        }
        
        .paste-area {
            background: #f5f5f7;
            border: 2px dashed #d1d1d6;
            border-radius: 16px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            transition: all 0.3s ease;
        }

        .paste-instruction {
            color: #86868b;
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 15px;
        }

        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(52, 199, 89, 0.1);
            color: #34C759;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 20px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background: #34C759;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }

        /* Responsive adjustments */
        @media (min-width: 1024px) {
            .stApp > div:nth-child(2) {
                flex-direction: row; /* Row layout for larger screens */
            }
            .sidebar-panel {
                min-height: calc(100vh - 40px);
            }
            .main-content-panel {
                min-height: calc(100vh - 40px);
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- Session State for managing data ---
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = parse_shopify_data("")
if 'recipient_email' not in st.session_state:
    st.session_state.recipient_email = ""
if 'email_subject' not in st.session_state:
    st.session_state.email_subject = ""
if 'email_body' not in st.session_state:
    st.session_state.email_body = ""
if 'show_status' not in st.session_state:
    st.session_state.show_status = False

# --- Layout the application ---
col1, col2 = st.columns([1, 2], gap="20px")

with col1: # Left Sidebar
    st.markdown('<div class="sidebar-panel">', unsafe_allow_html=True)
    st.markdown('<h1 class="app-title">Mail</h1>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">DAZZLE PREMIUM</p>', unsafe_allow_html=True)

    # Date and Time Display
    now = datetime.now()
    current_date = now.strftime('%A, %B %d, %Y')
    current_time = now.strftime('%I:%M:%S %p')
    st.markdown(f"""
        <div class="date-display">
            <div class="current-date">{current_date}</div>
            <div class="current-time">{current_time}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title"><div class="section-icon">📧</div> Mail Information</div>', unsafe_allow_html=True)

    # Missing Information Section
    if st.session_state.parsed_data["missing_info"]:
        st.markdown('<div class="missing-info">', unsafe_allow_html=True)
        st.markdown('<h3>⚠️ Missing Information</h3>', unsafe_allow_html=True)
        st.markdown('<ul class="missing-list">', unsafe_allow_html=True)
        for item in st.session_state.parsed_data["missing_info"]:
            st.markdown(f'<li>{item}</li>', unsafe_allow_html=True)
        st.markdown('</ul>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="paste-area">', unsafe_allow_html=True)
    st.markdown('<div class="paste-instruction">📋 Paste Order Data</div>', unsafe_allow_html=True)
    order_data_input = st.text_area(
        label="Paste your Shopify order export here...",
        value="",
        height=200,
        placeholder="Paste your Shopify order export here...",
        key="order_data_input_key" # Assign a key to manage state
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Update parsed data whenever the input changes
    if order_data_input != st.session_state.parsed_data.get('raw_text_input', ''): # Check if input actually changed
        st.session_state.parsed_data = parse_shopify_data(order_data_input)
        st.session_state.parsed_data['raw_text_input'] = order_data_input # Store current input for comparison
        # Reset email fields if input changes, as they might be outdated
        st.session_state.recipient_email = ""
        st.session_state.email_subject = ""
        st.session_state.email_body = ""
        st.session_state.show_status = False


    # Action Buttons
    if st.button("✨ Standard", help="Generate standard confirmation email"):
        data = st.session_state.parsed_data
        subject = f"Final Order Confirmation of dazzlepremium#{data['order_number']}"
        order_details = get_order_details_string(data['items'])
        message = f"""Hello {data['customer_name']},

This is DAZZLE PREMIUM Support confirming Order {data['order_number']}

- Please reply YES to confirm just this order only.
- Kindly also reply YES to the SMS sent automatically to your inbox.

Order Details:
{order_details}

For your security, we use two-factor authentication. If this order wasn't placed by you, text us immediately at 410-381-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""
        
        st.session_state.recipient_email = data['email_address']
        st.session_state.email_subject = subject
        st.session_state.email_body = message
        st.session_state.show_status = True

    if st.button("🚨 High Risk", help="Generate high-risk cancellation email"):
        data = st.session_state.parsed_data
        subject = "Important: Your DAZZLE PREMIUM Order - Action Required"
        message = f"""Hello {data['customer_name']},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we'd be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email.

Thank you,
DAZZLE PREMIUM Support"""
        
        st.session_state.recipient_email = data['email_address']
        st.session_state.email_subject = subject
        st.session_state.email_body = message
        st.session_state.show_status = True

    if st.button("↩️ Return", help="Generate return instructions email"):
        data = st.session_state.parsed_data
        subject = "DAZZLE PREMIUM: Your Return Request Instructions"
        message = f"""Dear {data['customer_name']},

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
        
        st.session_state.recipient_email = data['email_address']
        st.session_state.email_subject = subject
        st.session_state.email_body = message
        st.session_state.show_status = True
    
    st.markdown('</div>', unsafe_allow_html=True) # Close sidebar-panel div

with col2: # Main Mail Panel
    st.markdown('<div class="main-content-panel">', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="section-title">
            <div class="section-icon">✉️</div>
            Compose Email
            {
                '<div class="status-indicator" style="margin-left: auto;"><div class="status-dot"></div> Ready to Send</div>' 
                if st.session_state.show_status else ''
            }
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="mail-compose">', unsafe_allow_html=True)
    st.markdown('<div class="compose-header">', unsafe_allow_html=True)
    
    # Recipient Email
    st.markdown('<label class="form-label" for="recipientEmail">To:</label>', unsafe_allow_html=True)
    st.text_input(
        label="To:",
        value=st.session_state.recipient_email,
        key="recipient_email_input",
        placeholder="Recipient email address",
        disabled=True
    )
    
    # Email Subject
    st.markdown('<label class="form-label" for="emailSubject">Subject:</label>', unsafe_allow_html=True)
    st.text_input(
        label="Subject:",
        value=st.session_state.email_subject,
        key="email_subject_input",
        placeholder="Email subject line",
        disabled=True
    )
    st.markdown('</div>', unsafe_allow_html=True) # Close compose-header div

    st.markdown('<div class="compose-body">', unsafe_allow_html=True)
    st.markdown('<label class="form-label" for="emailBody">Message:</label>', unsafe_allow_html=True)
    st.text_area(
        label="Message:",
        value=st.session_state.email_body,
        height=400,
        key="email_body_input",
        placeholder="Email message will appear here...",
        disabled=True
    )
    st.markdown('</div>', unsafe_allow_html=True) # Close compose-body div
    st.markdown('</div>', unsafe_allow_html=True) # Close mail-compose div
    st.markdown('</div>', unsafe_allow_html=True) # Close main-content-panel div
