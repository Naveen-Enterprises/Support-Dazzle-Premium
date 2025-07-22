import streamlit as st
import re
import time

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="wide")

# Initialize session state
if "email_generated" not in st.session_state:
    st.session_state.email_generated = False
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "processing" not in st.session_state:
    st.session_state.processing = False

# --- Apple-Inspired Design System ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700;800&family=SF+Pro+Text:wght@300;400;500;600&display=swap');
    
    :root {
        --apple-blue: #007AFF;
        --apple-blue-hover: #0056CC;
        --apple-blue-active: #004499;
        --apple-gray-1: #F2F2F7;
        --apple-gray-2: #E5E5EA;
        --apple-gray-3: #C7C7CC;
        --apple-gray-4: #D1D1D6;
        --apple-gray-5: #8E8E93;
        --apple-gray-6: #636366;
        --apple-text-primary: #000000;
        --apple-text-secondary: #3C3C43;
        --apple-green: #30D158;
        --apple-red: #FF3B30;
        --apple-orange: #FF9500;
        --apple-surface: #FFFFFF;
        --apple-surface-secondary: #F2F2F7;
    }
    
    * {
        font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }
    
    .main {
        background: var(--apple-surface);
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0;
    }
    
    .stApp {
        background: var(--apple-surface-secondary);
    }
    
    /* Hero Section */
    .hero-section {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%);
        color: white;
        text-align: center;
        padding: 4rem 2rem;
        margin: -2rem -2rem 3rem -2rem;
        border-radius: 0 0 24px 24px;
    }
    
    .hero-title {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: clamp(2.5rem, 5vw, 4rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        opacity: 0.8;
        margin-bottom: 0;
    }
    
    /* Card System */
    .card {
        background: var(--apple-surface);
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.05), 0 1px 6px rgba(0, 0, 0, 0.02);
        border: 1px solid var(--apple-gray-2);
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1.5rem;
    }
    
    .card:hover {
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.1), 0 2px 12px rgba(0, 0, 0, 0.04);
        transform: translateY(-2px);
    }
    
    .card-header {
        padding: 1.5rem 2rem 0 2rem;
        border-bottom: none;
    }
    
    .card-title {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--apple-text-primary);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .card-subtitle {
        color: var(--apple-text-secondary);
        font-size: 1rem;
        font-weight: 400;
        opacity: 0.8;
    }
    
    .card-body {
        padding: 1.5rem 2rem 2rem 2rem;
    }
    
    /* Input Fields */
    .stTextArea textarea {
        font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        padding: 1.25rem !important;
        border: 2px solid var(--apple-gray-2) !important;
        border-radius: 12px !important;
        background: var(--apple-surface) !important;
        color: var(--apple-text-primary) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        resize: vertical !important;
        box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.04) !important;
    }
    
    .stTextArea textarea:focus {
        border-color: var(--apple-blue) !important;
        box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.04), 0 0 0 4px rgba(0, 122, 255, 0.15) !important;
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--apple-gray-5) !important;
        font-style: italic;
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 1rem;
        animation: slideInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .status-ready {
        background: rgba(48, 209, 88, 0.1);
        color: var(--apple-green);
        border: 1px solid rgba(48, 209, 88, 0.2);
    }
    
    .status-warning {
        background: rgba(255, 149, 0, 0.1);
        color: var(--apple-orange);
        border: 1px solid rgba(255, 149, 0, 0.2);
    }
    
    .status-processing {
        background: rgba(0, 122, 255, 0.1);
        color: var(--apple-blue);
        border: 1px solid rgba(0, 122, 255, 0.2);
    }
    
    /* Info Chips */
    .info-chip {
        background: var(--apple-surface-secondary);
        border: 1px solid var(--apple-gray-2);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 1rem;
        font-family: 'SF Mono', Monaco, monospace;
        font-size: 0.95rem;
        color: var(--apple-text-primary);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    
    .info-chip::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--apple-blue);
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .info-chip:hover::before {
        transform: translateX(0);
    }
    
    .info-chip-label {
        font-size: 0.8rem;
        color: var(--apple-gray-6);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    /* Code Block */
    .stCode {
        border-radius: 12px !important;
        border: 1px solid var(--apple-gray-2) !important;
        background: var(--apple-surface-secondary) !important;
        font-family: 'SF Mono', Monaco, monospace !important;
        font-size: 0.9rem !important;
        line-height: 1.5 !important;
        box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.04) !important;
    }
    
    /* Buttons */
    .stButton button {
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, sans-serif !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.875rem 2rem !important;
        border-radius: 12px !important;
        border: none !important;
        background: var(--apple-blue) !important;
        color: white !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(0, 122, 255, 0.25) !important;
        letter-spacing: -0.01em !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        background: var(--apple-blue-hover) !important;
        box-shadow: 0 6px 20px rgba(0, 122, 255, 0.35) !important;
        transform: translateY(-1px) !important;
    }
    
    .stButton button:active {
        background: var(--apple-blue-active) !important;
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2) !important;
    }
    
    /* Secondary Button */
    .secondary-button button {
        background: var(--apple-surface) !important;
        color: var(--apple-text-primary) !important;
        border: 2px solid var(--apple-gray-2) !important;
        box-shadow: none !important;
    }
    
    .secondary-button button:hover {
        background: var(--apple-surface-secondary) !important;
        border-color: var(--apple-gray-3) !important;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08) !important;
    }
    
    /* Animations */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .animate-in {
        animation: slideInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Processing Animation */
    .processing-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid var(--apple-blue);
        border-radius: 50%;
        border-top: 2px solid transparent;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-section {
            padding: 3rem 1rem;
        }
        
        .card-body {
            padding: 1rem 1.5rem 1.5rem 1.5rem;
        }
        
        .hero-title {
            font-size: 2.5rem;
        }
    }
    
    /* Hide Streamlit Elements */
    .stDeployButton { display: none; }
    footer { display: none; }
    header { display: none; }
    
    /* Grid Layout */
    .main-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    @media (max-width: 968px) {
        .main-grid {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

def extract_order_data(raw_text):
    """Extract order data with improved parsing"""
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
        if re.search(r" - [A-Z0-9\-]+$", line) and not any(skip in line for skip in ["SKU", "Discount"]):
            product_line = line
            product_name, style_code = product_line.rsplit(" - ", 1)
            size = "[Size Not Found]"

            for offset in range(1, 5):
                if i + offset < len(lines):
                    size_line = lines[i + offset].strip()
                    size_match_num = re.match(r"^(\d{1,2})", size_line)
                    if size_match_num:
                        size = size_match_num.group(1).strip()
                        break
                    size_match_letters = re.match(r"^[XSML]{1,2}[XS]?", size_line)
                    if size_match_letters:
                        size = size_match_letters.group(0).strip()
                        break
                    if not size_line.startswith("$") and not size_line.startswith("SKU") and len(size_line.split()) == 1 and len(size_line) > 0 and len(size_line) < 10:
                        size = size_line
                        break
            
            items.append((product_name.strip(), style_code.strip(), size))
        i += 1

    return {
        "customer_name": customer_name,
        "email_address": email_address,
        "phone_number": phone_number,
        "order_number": order_number,
        "items": items
    }

def generate_email_content(order_data, is_high_risk=False):
    """Generate email content based on order data"""
    if is_high_risk:
        return f"""Hello {order_data['customer_name']},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we'd be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email."""
    
    # Regular email
    order_details_list = []
    for idx, (p, s, z) in enumerate(order_data['items']):
        item_prefix = ""
        if len(order_data['items']) > 1:
            item_prefix = f"- Item {idx+1}:\n"
        
        item_detail = f"{item_prefix}• Product: {p}\n• Size: {z}"
        
        if len(order_data['items']) > 1:
            item_detail += f"\n• Style Code: {s}"
        order_details_list.append(item_detail)

    order_details = "\n\n".join(order_details_list)
    
    message_lines = [
        f"Hello {order_data['customer_name']},",
        "", 
        f"This is DAZZLE PREMIUM Support confirming Order {order_data['order_number']}",
        "", 
        "- Please reply YES to confirm just this order only.",
        "- Kindly also reply YES to the SMS sent automatically to your inbox.",
        "", 
        "Order Details:",
        order_details,
        "", 
        "For your security, we use two-factor authentication. If this order wasn't placed by you, text us immediately at 410-381-0000 to cancel.",
        "", 
        "Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.",
        "", 
        "If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.",
        "Thank you for choosing DAZZLE PREMIUM!"
    ]
    
    return "\n".join(message_lines)

def validate_order_data(order_data):
    """Validate extracted order data and return missing fields"""
    missing_info = []
    if "[Customer Name Not Found]" in order_data['customer_name']: 
        missing_info.append("Customer Name")
    if "[Email Not Found]" in order_data['email_address']: 
        missing_info.append("Email Address")
    if "[Phone Not Found]" in order_data['phone_number']: 
        missing_info.append("Phone Number")
    if "[Order # Not Found]" in order_data['order_number']: 
        missing_info.append("Order Number")
    if any("[Size Not Found]" in item[2] for item in order_data['items']): 
        missing_info.append("Item Sizes")
    
    return missing_info

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">DAZZLE PREMIUM</h1>
    <p class="hero-subtitle">Intelligent Order Email Generator</p>
</div>
""", unsafe_allow_html=True)

# Main Layout
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# Left Column - Input
with st.container():
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <h2 class="card-title">📦 Order Input</h2>
            <p class="card-subtitle">Paste your Shopify export and watch the magic happen</p>
        </div>
        <div class="card-body">
    """, unsafe_allow_html=True)
    
    # Smart input with instant processing
    raw_text = st.text_area(
        "",
        height=400,
        placeholder="Paste your complete Shopify order export here...\n\nThe email will generate automatically as you paste.",
        key="order_input",
        help="Simply paste the order details and the email will be generated instantly"
    )
    
    # Action Buttons
    col1, col2 = st.columns(2)
    with col1:
        high_risk_clicked = st.button("⚠️ High-Risk Email")
    with col2:
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        new_order_clicked = st.button("✨ New Order")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# Right Column - Output
with st.container():
    if raw_text.strip():
        # Process the order data
        order_data = extract_order_data(raw_text)
        missing_info = validate_order_data(order_data)
        
        # Determine email type
        is_high_risk = high_risk_clicked and raw_text.strip()
        email_content = generate_email_content(order_data, is_high_risk)
        subject = f"Final Order Confirmation of dazzlepremium#{order_data['order_number']}"
        
        # Status indicator
        if is_high_risk:
            status_html = '<div class="status-indicator status-warning"><span>⚠️</span> High-Risk Email Generated</div>'
        elif missing_info:
            status_html = f'<div class="status-indicator status-warning"><span>⚠️</span> Please verify: {", ".join(missing_info)}</div>'
        else:
            status_html = '<div class="status-indicator status-ready"><span>✅</span> Email Ready</div>'
        
        st.markdown(f"""
        <div class="card animate-in">
            <div class="card-header">
                <h2 class="card-title">✉️ Generated Email</h2>
                <p class="card-subtitle">Ready to copy and send</p>
            </div>
            <div class="card-body">
                {status_html}
        """, unsafe_allow_html=True)
        
        # Email details
        st.markdown(f"""
        <div class="info-chip">
            <div class="info-chip-label">Email Address</div>
            <div>{order_data['email_address']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-chip">
            <div class="info-chip-label">Subject Line</div>
            <div>{subject}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1.5rem 0 0.5rem 0;"><strong>📋 Email Body</strong></div>', unsafe_allow_html=True)
        st.code(email_content, language="text")
        
        st.markdown(f"""
        <div class="info-chip">
            <div class="info-chip-label">Phone Number</div>
            <div>{order_data['phone_number']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
    else:
        # Empty state with helpful guidance
        st.markdown("""
        <div class="card">
            <div class="card-body" style="text-align: center; padding: 4rem 2rem;">
                <h3 style="color: var(--apple-gray-5); font-weight: 400; margin-bottom: 1rem;">
                    Ready to generate your email
                </h3>
                <p style="color: var(--apple-gray-5); font-size: 1.1rem; line-height: 1.6;">
                    Paste your Shopify order export in the input field<br>
                    and your professional email will appear instantly.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle new order reset
if new_order_clicked:
    st.rerun()
