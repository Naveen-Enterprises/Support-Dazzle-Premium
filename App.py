import streamlit as st
import re
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mail - DAZZLE PREMIUM",
    page_icon="📧",
    layout="centered", # Centered layout for a focused, app-like feel
    initial_sidebar_state="collapsed" # Collapsed sidebar for a cleaner look
)

# Custom CSS for a polished, minimalist, and "Apple-like" aesthetic
st.markdown("""
<style>
    /* General body and main content styling */
    body {
        font-family: 'Inter', sans-serif;
        background-color: #f0f2f6; /* Very light gray background */
        color: #333; /* Dark gray text */
        -webkit-font-smoothing: antialiased; /* Smoother fonts */
        -moz-osx-font-smoothing: grayscale;
    }
    .main > div {
        max-width: 900px; /* Optimal width for readability and focus */
        padding: 2.5rem; /* Generous padding inside the main card */
        margin: 2.5rem auto; /* Center the content with more vertical margin */
        background-color: #ffffff; /* Pure white background for the main card */
        border-radius: 16px; /* Significantly more rounded corners */
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08); /* Enhanced, softer shadow for depth */
        border: 1px solid #e8e8e8; /* Very subtle border for definition */
    }

    /* Streamlit header and info box */
    .stApp > header {
        display: none; /* Hide Streamlit's default header */
    }
    .stApp {
        padding-top: 0 !important;
    }
    .stAlert {
        border-radius: 10px; /* Rounded corners for alerts */
        padding: 1rem 1.5rem;
        font-size: 0.95rem;
        margin-bottom: 1.5rem; /* Increased consistent spacing below alerts */
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05); /* Subtle shadow for alerts */
    }
    .stAlert.info {
        background-color: #e0f7fa; /* Light cyan */
        color: #006064; /* Dark cyan text */
        border-left: 5px solid #00bcd4; /* Cyan border */
    }
    .stAlert.warning {
        background-color: #fff3cd;
        color: #856404;
        border-left: 5px solid #ffc107;
    }
    .stAlert.success {
        background-color: #d4edda;
        color: #155724;
        border-left: 5px solid #28a745;
    }

    /* Text Areas and Text Inputs */
    .stTextArea textarea, .stTextInput input {
        border: 1px solid #e0e0e0; /* Light gray border */
        border-radius: 10px; /* Rounded input fields */
        padding: 0.85rem 1.1rem; /* More generous padding */
        font-size: 1rem;
        transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        margin-bottom: 1.25rem; /* Consistent spacing */
        background-color: #fcfcfc; /* Slightly off-white background for inputs */
    }
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #007aff; /* Apple-like blue focus border */
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2); /* Soft, subtle focus glow */
        outline: none;
    }
    .stTextInput label, .stTextArea label {
        font-weight: 500; /* Medium weight labels */
        color: #555;
        margin-bottom: 0.6rem; /* Space between label and input */
        display: block; /* Ensure label is on its own line */
        font-size: 0.95rem;
    }

    /* Buttons */
    .stButton > button {
        background-color: #007aff; /* Primary Apple-like blue */
        color: white;
        border: none;
        border-radius: 10px; /* Rounded buttons */
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        font-weight: 600; /* Semibold */
        cursor: pointer;
        transition: background-color 0.2s ease-in-out, transform 0.1s ease-in-out, box-shadow 0.2s ease-in-out;
        margin-bottom: 1rem; /* Consistent spacing */
        box-shadow: 0 4px 15px rgba(0, 122, 255, 0.2); /* Soft shadow for primary buttons */
    }
    .stButton > button:hover {
        background-color: #005bb5; /* Darker blue on hover */
        transform: translateY(-2px); /* More noticeable lift effect */
        box-shadow: 0 6px 20px rgba(0, 122, 255, 0.3);
    }
    .stButton > button.css-1x8b0s { /* Target primary button specifically */
        background-color: #007aff;
    }
    .stButton > button.css-1x8b0s:hover {
        background-color: #005bb5;
    }
    /* Style for secondary buttons (High Risk, Return) */
    .stButton > button:not(.css-1x8b0s) { /* Target non-primary buttons */
        background-color: #f0f2f6; /* Very light background */
        color: #555;
        border: 1px solid #dcdcdc; /* Light border */
        box-shadow: none;
    }
    .stButton > button:not(.css-1x8b0s):hover {
        background-color: #e8e8e8; /* Slightly darker on hover */
        color: #333;
        transform: translateY(-1px);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    /* Section Headers */
    h1, h3, h4, h5 {
        color: #333;
        margin-top: 2rem; /* More space above sections */
        margin-bottom: 1rem;
        font-weight: 700; /* Bolder headers */
    }
    h1 { font-size: 2.5rem; margin-bottom: 1.5rem; color: #1a1a1a; } /* Larger, darker main title */
    h3 { font-size: 2rem; }
    h4 { font-size: 1.6rem; }
    h5 { font-size: 1.3rem; }

    /* Custom Sections (Missing Info, Notes) */
    .card-section {
        background-color: #fcfcfc; /* Very light gray for internal cards */
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #f0f0f0; /* Very subtle border */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03); /* Extremely subtle shadow */
    }
    .card-section.warning-style {
        background-color: #fff3cd; /* Light yellow for warnings */
        border-left: 5px solid #ffc107;
        border: none; /* Remove subtle border if left border is present */
        box-shadow: none; /* Remove subtle shadow for warning style */
    }
    .card-section h4 {
        color: #856404;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }
    .card-section ul {
        margin: 0;
        padding-left: 1.25rem;
        list-style-type: disc;
        color: #555;
    }
    .notes-card-style {
        background-color: #e6f7ff; /* Light blue */
        border-left: 5px solid #3399ff;
        border: none;
        box-shadow: none;
    }
    .notes-card-style h5 {
        color: #004085;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 4rem; /* More space above footer */
        padding-top: 2rem;
        border-top: 1px solid #e0e0e0;
        color: #888;
        font-size: 0.9rem;
    }
    .stMarkdown p {
        margin-bottom: 1rem; /* Ensure consistent spacing for paragraphs */
    }
    .stMarkdown h4 {
        margin-bottom: 0.75rem; /* Tighter spacing for sub-headers */
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None
if 'email_generated' not in st.session_state:
    st.session_state.email_generated = False
if 'email_data' not in st.session_state:
    st.session_state.email_data = (None, None, None)
if 'is_data_available' not in st.session_state: # Tracks if parsed data is available
    st.session_state.is_data_available = False
if 'last_order_input_value_for_parsing' not in st.session_state: # Stores last input for change detection
    st.session_state.last_order_input_value_for_parsing = ''

# Session state for order notes
if 'order_notes' not in st.session_state:
    st.session_state.order_notes = {} # Dictionary to store notes, keyed by order number


def parse_shopify_data(raw_text):
    """
    Parse Shopify order data from raw text using more robust regex.
    This version correctly handles multi-line item details including size.
    """
    data = {
        "customer_name": "[Customer Name Not Found]",
        "email_address": "[Email Not Found]",
        "phone_number": "[Phone Not Found]",
        "order_number": "[Order # Not Found]",
        "items": [],
        "missing_info": []
    }

    if not raw_text or not raw_text.strip():
        return None # Return None if input is empty

    # Extract customer name
    name_match = re.search(r'Order confirmation email was sent to (.*?)\s*\(', raw_text, re.IGNORECASE)
    if name_match:
        data["customer_name"] = name_match.group(1).strip()
    else:
        # Fallback for customer name
        name_fallback_match = re.search(r'Customer\n\n(.*?)\n', raw_text)
        if name_fallback_match:
            data["customer_name"] = name_fallback_match.group(1).strip()
        else:
            data["missing_info"].append("Customer Name")


    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.[\w\.-]+', raw_text)
    if email_match:
        data["email_address"] = email_match.group(0).strip()
    else:
        data["missing_info"].append("Email Address")

    # Extract phone
    phone_match = re.search(r'\+1[ \d\-()]{10,}', raw_text)
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

    # Extract items using a more reliable, line-by-line method
    lines = [line.strip() for line in raw_text.split('\n')]
    for i, line in enumerate(lines):
        # Find items by looking for the SKU, which is a consistent marker
        if line.startswith("SKU:") and i > 1 and i < len(lines) - 1:
            try:
                product_line = lines[i-2]
                size_line = lines[i-1]
                quantity_line = lines[i+1]

                # Product Name and Style Code
                product_match = re.match(r'(.*) - (.*)', product_line)
                product_name = product_match.group(1).strip() if product_match else product_line
                style_code = product_match.group(2).strip() if product_match else "[Style Code Not Found]"

                # Size
                size = size_line.split('/')[0].strip() if '/' in size_line else size_line

                # Quantity
                quantity_match = re.search(r'×\s*(\d+)', quantity_line)
                quantity = int(quantity_match.group(1)) if quantity_match else 1
                
                data["items"].append({
                    "product_name": product_name,
                    "style_code": style_code,
                    "size": size,
                    "quantity": quantity
                })
            except (IndexError, AttributeError):
                # Could not parse this item, skip it
                continue
    
    if not data["items"]:
        data["missing_info"].append("Order Items")

    return data

def generate_email_content(parsed_data, email_type):
    """Single function to generate different email types."""
    message = ""
    subject = ""

    if email_type == "standard":
        subject = f"Final Order Confirmation of dazzlepremium#{parsed_data['order_number']}"
        order_details = ""
        if parsed_data["items"]:
            for idx, item in enumerate(parsed_data["items"]):
                order_details += f"- Item {idx + 1}:\n"
                order_details += f"•  Product: {item['product_name']}\n"
                order_details += f"•  Style Code: {item['style_code']}\n"
                order_details += f"•  Size: {item['size']}"
                if item["quantity"] > 1:
                    order_details += f"\n•  Quantity: {item['quantity']}"
                order_details += "\n\n"
        else:
            order_details = "No items found."

        message = f"""Hello {parsed_data['customer_name']},

This is DAZZLE PREMIUM Support confirming Order {parsed_data['order_number']}

- Please reply YES to confirm just this order only.
- Kindly also reply YES to the SMS sent automatically to your inbox.

Order Details:
{order_details.strip()}

For your security, we use two-factor authentication. If this order wasn't placed by you, text us immediately at 410-381-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!"""

    elif email_type == "high_risk":
        subject = "Important: Your DAZZLE PREMIUM Order - Action Required"
        message = f"""Hello {parsed_data['customer_name']},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we'd be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel feel to reply to this email.

Thank you,
DAZZLE PREMIUM Support"""

    elif email_type == "return":
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

# --- Main App Layout ---
st.title("📧 Mail - DAZZLE PREMIUM")
st.markdown("### Premium Email Generator")

current_time = datetime.now()
st.info(f"📅 {current_time.strftime('%A, %B %d, %Y')} | 🕒 {current_time.strftime('%I:%M:%S %p')}")

# Use a single container for the main two-column layout
with st.container():
    col1, col2 = st.columns([1, 2]) # Keep the 1:2 ratio for input/output

    with col1:
        st.markdown("#### 📋 Paste Shopify Order Data")
        
        order_data = st.text_area(
            "The email will generate automatically below once you paste the data.",
            height=350,
            placeholder="Paste your full Shopify order page content here...",
            key="order_input"
        )
        
        # Seamlessly parse data on input change, but only if content actually changed
        if order_data != st.session_state.last_order_input_value_for_parsing:
            st.session_state.parsed_data = parse_shopify_data(order_data)
            st.session_state.last_order_input_value_for_parsing = order_data
            
            # Update data availability state based on parsing result
            st.session_state.is_data_available = (st.session_state.parsed_data is not None)
            
            # Reset email generation state if input changes
            st.session_state.email_generated = False
            st.session_state.email_data = (None, None, None)
        elif not order_data and st.session_state.is_data_available: # If order_data is now empty, clear parsed data and reset state
            st.session_state.parsed_data = None
            st.session_state.is_data_available = False
            st.session_state.email_generated = False
            st.session_state.email_data = (None, None, None)
            st.session_state.last_order_input_value_for_parsing = '' # Clear last input value
        
        # Display missing information if parsing occurred and there are issues
        if st.session_state.parsed_data and st.session_state.parsed_data.get("missing_info"):
            st.markdown('<div class="card-section warning-style"><h4>⚠️ Missing Information</h4><ul>', unsafe_allow_html=True)
            for item in st.session_state.parsed_data["missing_info"]:
                st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)
        
        st.markdown("#### ✨ Generate Email")
        
        # Email generation buttons
        col1a, col1b, col1c = st.columns(3)
        
        def handle_email_generation(email_type):
            # Ensure parsed data is available before generating email
            if st.session_state.is_data_available and st.session_state.parsed_data:
                st.session_state.email_data = generate_email_content(st.session_state.parsed_data, email_type)
                st.session_state.email_generated = True
            else:
                st.warning("Please paste valid order data first to generate an email!")

        with col1a:
            st.button("✨ Standard", on_click=handle_email_generation, args=("standard",), use_container_width=True, type="primary")
        
        with col1b:
            st.button("🚨 High Risk", on_click=handle_email_generation, args=("high_risk",), use_container_width=True)
        
        with col1c:
            st.button("↩️ Return", on_click=handle_email_generation, args=("return",), use_container_width=True)

        # Order Notes section (always visible)
        current_order_number = st.session_state.parsed_data["order_number"] if st.session_state.parsed_data else "No Order"
        
        # Initialize note for current order if not exists
        if current_order_number not in st.session_state.order_notes:
            st.session_state.order_notes[current_order_number] = ""

        st.markdown(f'<div class="card-section notes-card-style"><h5>📝 Notes for Order: {current_order_number}</h5>', unsafe_allow_html=True)
        
        # Order notes text area
        st.session_state.order_notes[current_order_number] = st.text_area(
            "Add your tracking notes here:",
            value=st.session_state.order_notes.get(current_order_number, ""),
            height=150,
            placeholder="e.g., 'Follow-up needed', 'Called customer about size issue'",
            key=f"order_notes_text_area_{current_order_number}" # Unique key for each order
        )
        st.markdown('</div>', unsafe_allow_html=True)


    with col2:
        st.markdown("#### ✉️ Compose Email")
        
        email_to, email_subject, email_body = st.session_state.get('email_data', (None, None, None))

        if st.session_state.email_generated and all(st.session_state.email_data):
            st.markdown('<div class="stAlert success"><strong>✅ Email Generated Successfully!</strong></div>', unsafe_allow_html=True)
            
            st.text_input("To:", value=email_to, key="email_to")
            st.text_input("Subject:", value=email_subject, key="email_subject")
            st.text_area("Message:", value=email_body, height=400, key="email_body")
        
        else:
            st.info("👆 Paste order data and select an email type to generate the content.")
            
            # Placeholder fields
            st.text_input("To:", placeholder="Recipient email will appear here", disabled=True)
            st.text_input("Subject:", placeholder="Email subject will appear here", disabled=True)
            st.text_area("Message:", placeholder="Email message will appear here...", height=400, disabled=True)

# Footer
st.markdown('<div class="footer">**DAZZLE PREMIUM** - Premium Email Management System</div>', unsafe_allow_html=True)
