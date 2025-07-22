import streamlit as st
import re
import json # Import the json module for robust string escaping
import time # For simulating processing feedback

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="wide")

# Initialize session state for UI control and data persistence
if "email_generated" not in st.session_state:
    st.session_state.email_generated = False
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "processing" not in st.session_state:
    st.session_state.processing = False
if "generated_email_body" not in st.session_state:
    st.session_state.generated_email_body = ""
if "current_subject" not in st.session_state:
    st.session_state.current_subject = "[Subject Not Generated]"
if "current_email_address" not in st.session_state:
    st.session_state.current_email_address = "[Email Not Found]"
if "current_phone_number" not in st.session_state:
    st.session_state.current_phone_number = "[Phone Not Found]"


# --- Apple-Inspired Design System ---
st.markdown("""
<style>
    /* Import Apple's SF Pro fonts (approximation via Google Fonts) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Define Apple-like color palette and typography variables */
    :root {
        --apple-blue: #007AFF;
        --apple-blue-hover: #0056CC;
        --apple-blue-active: #004499;
        --apple-gray-1: #F2F2F7; /* Lightest background */
        --apple-gray-2: #E5E5EA; /* Light border/separator */
        --apple-gray-3: #C7C7CC; /* Medium border/placeholder */
        --apple-gray-4: #D1D1D6;
        --apple-gray-5: #8E8E93; /* Secondary text */
        --apple-gray-6: #636366; /* Tertiary text */
        --apple-text-primary: #000000;
        --apple-text-secondary: #3C3C43;
        --apple-green: #30D158; /* Success */
        --apple-red: #FF3B30; /* Error/High-Risk */
        --apple-orange: #FF9500; /* Warning */
        --apple-surface: #FFFFFF; /* Card/main background */
        --apple-surface-secondary: #F2F2F7; /* Input/secondary background */
    }
    
    /* Global font smoothing and rendering for crisp text */
    * {
        font-feature-settings: "kern" 1, "liga" 1, "calt" 1;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-rendering: optimizeLegibility;
    }
    
    /* Main Streamlit container styling */
    .main {
        background: var(--apple-surface);
        font-family: 'Inter', sans-serif; /* Using Inter as SF Pro approximation */
        max-width: 1200px;
        margin: 0 auto;
        padding: 0; /* Remove default padding from .main */
        border-radius: 24px; /* Consistent large border-radius */
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08); /* Soft, deep shadow */
        border: 1px solid var(--apple-gray-2); /* Subtle outer border */
    }
    
    /* Streamlit app background */
    .stApp {
        background: linear-gradient(180deg, var(--apple-gray-1) 0%, var(--apple-gray-2) 100%); /* Subtle gradient background for the whole app */
    }
    
    /* Hero Section - Top banner */
    .hero-section {
        background: linear-gradient(180deg, #000000 0%, #1a1a1a 100%); /* Dark, sleek gradient */
        color: white;
        text-align: center;
        padding: 4rem 2rem;
        /* Negative margin to extend beyond .main padding */
        margin: -3.5rem -3.5rem 3rem -3.5rem; 
        border-radius: 23px 23px 0 0; /* Rounded top corners, sharp bottom */
    }
    
    .hero-title {
        font-family: 'Inter', sans-serif; /* SF Pro Display equivalent */
        font-size: clamp(2.5rem, 5vw, 4rem); /* Responsive font size */
        font-weight: 800; /* Extra bold for impact */
        letter-spacing: -0.03em; /* Tighter letter spacing */
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%); /* White gradient text */
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
    
    /* Card System - General styling for content blocks */
    .card {
        background: var(--apple-surface);
        border-radius: 16px; /* Slightly smaller than main for nested elements */
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03), 0 1px 6px rgba(0, 0, 0, 0.01); /* Lighter shadow for cards */
        border: 1px solid var(--apple-gray-2);
        overflow: hidden;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem; /* More spacing between cards */
    }
    
    .card:hover {
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.07), 0 2px 12px rgba(0, 0, 0, 0.03);
        transform: translateY(-3px); /* More pronounced lift on hover */
    }
    
    .card-header {
        padding: 1.75rem 2.5rem 0 2.5rem; /* More padding */
        border-bottom: none;
    }
    
    .card-title {
        font-family: 'Inter', sans-serif; /* SF Pro Display equivalent */
        font-size: 1.8rem; /* Larger card titles */
        font-weight: 700; /* Bold */
        color: var(--apple-text-primary);
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    }
    
    .card-subtitle {
        color: var(--apple-gray-5);
        font-size: 1.05rem;
        font-weight: 400;
        margin-bottom: 1.5rem; /* More spacing */
    }
    
    .card-body {
        padding: 0 2.5rem 2.5rem 2.5rem; /* Consistent padding */
    }
    
    /* Input Fields (Text Area) */
    .stTextArea textarea {
        font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, monospace !important;
        font-size: 0.98rem !important; /* Slightly larger monospace font */
        line-height: 1.6 !important;
        padding: 1.5rem !important; /* Generous padding */
        border: 2px solid var(--apple-gray-3) !important; /* More visible border */
        border-radius: 14px !important; /* More rounded */
        background: var(--apple-surface-secondary) !important; /* Light gray background */
        color: var(--apple-text-primary) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        resize: vertical !important;
        box-shadow: inset 0 1px 6px rgba(0, 0, 0, 0.06) !important; /* Deeper inner shadow */
    }
    
    .stTextArea textarea:focus {
        border-color: var(--apple-blue) !important;
        box-shadow: inset 0 1px 6px rgba(0, 0, 0, 0.06), 0 0 0 5px rgba(0, 122, 255, 0.2) !important; /* Stronger glow */
        outline: none !important;
    }
    
    .stTextArea textarea::placeholder {
        color: var(--apple-gray-5) !important;
        font-style: italic;
    }
    
    /* Status Indicators (Success, Warning, Processing) */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.7rem 1.4rem; /* More padding */
        border-radius: 24px; /* Pill shape */
        font-size: 1rem; /* Larger font */
        font-weight: 600;
        margin-bottom: 1.5rem; /* More spacing */
        animation: slideInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .status-ready {
        background: rgba(48, 209, 88, 0.15); /* Richer background */
        color: var(--apple-green);
        border: 1px solid rgba(48, 209, 88, 0.3);
    }
    
    .status-warning {
        background: rgba(255, 149, 0, 0.15);
        color: var(--apple-orange);
        border: 1px solid rgba(255, 149, 0, 0.3);
    }
    
    .status-processing {
        background: rgba(0, 122, 255, 0.15);
        color: var(--apple-blue);
        border: 1px solid rgba(0, 122, 255, 0.3);
    }
    
    /* Info Chips (Email, Subject, Phone) */
    .info-chip {
        background: var(--apple-surface-secondary);
        border: 1px solid var(--apple-gray-2);
        border-radius: 16px; /* Consistent rounding */
        padding: 1.25rem 1.75rem; /* More padding */
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif; /* SF Pro Text for data */
        font-size: 1.05rem;
        color: var(--apple-text-primary);
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03); /* Subtle shadow */
    }
    
    .info-chip::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px; /* Thicker accent line */
        background: var(--apple-blue);
        transform: translateX(-100%);
        transition: transform 0.3s ease-out; /* Smoother transition */
    }
    
    .info-chip:hover::before {
        transform: translateX(0);
    }
    
    .info-chip-label {
        font-size: 0.85rem; /* Slightly larger label */
        color: var(--apple-gray-5);
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.06em; /* More pronounced letter spacing */
        margin-bottom: 0.4rem; /* More spacing */
    }
    
    /* Code Block for Email Body Display */
    .stCode {
        border-radius: 12px !important;
        border: 1px solid var(--apple-gray-3) !important; /* More defined border */
        background: var(--apple-surface) !important; /* White background for code */
        font-family: 'SF Mono', Monaco, monospace !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
        box-shadow: inset 0 1px 4px rgba(0, 0, 0, 0.05) !important; /* Inner shadow */
        padding: 1.5rem !important; /* More padding */
        color: var(--apple-text-primary) !important;
    }
    
    /* Buttons - Primary & Secondary */
    .stButton button {
        font-family: 'Inter', sans-serif !important; /* Consistent font */
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        padding: 1rem 2.2rem !important; /* Generous padding */
        border-radius: 12px !important;
        border: none !important;
        background: var(--apple-blue) !important;
        color: white !important;
        cursor: pointer !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 5px 20px rgba(0, 122, 255, 0.3) !important;
        letter-spacing: -0.01em !important;
        width: 100% !important; /* Full width buttons */
    }
    
    .stButton button:hover {
        background: var(--apple-blue-hover) !important;
        box-shadow: 0 8px 25px rgba(0, 122, 255, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton button:active {
        background: var(--apple-blue-active) !important;
        transform: translateY(0) !important;
        box-shadow: 0 2px 8px rgba(0, 122, 255, 0.2) !important;
    }
    
    /* Secondary Button Style */
    .secondary-button button {
        background: var(--apple-surface) !important;
        color: var(--apple-text-primary) !important;
        border: 2px solid var(--apple-gray-3) !important; /* Clearer border */
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05) !important; /* Subtle shadow */
    }
    
    .secondary-button button:hover {
        background: var(--apple-surface-secondary) !important;
        border-color: var(--apple-gray-4) !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
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
        animation: slideInUp 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94); /* Smoother cubic-bezier */
    }
    
    /* Processing Animation */
    .processing-spinner {
        display: inline-block;
        width: 18px; /* Larger spinner */
        height: 18px;
        border: 3px solid var(--apple-blue); /* Thicker spinner */
        border-radius: 50%;
        border-top: 3px solid transparent;
        animation: spin 0.8s linear infinite; /* Faster spin */
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Responsive Design */
    @media (max-width: 992px) { /* Adjusted breakpoint for tablets */
        .main-grid {
            grid-template-columns: 1fr;
            gap: 2rem;
            padding: 0 1.5rem; /* More padding on smaller screens */
        }
        .main {
            padding: 2.5rem;
            margin: 1.5rem auto;
        }
        .hero-section {
            padding: 3rem 1.5rem;
            margin: -2.5rem -2.5rem 2.5rem -2.5rem;
        }
        .hero-title {
            font-size: 3rem;
        }
        .card-header {
            padding: 1.5rem 2rem 0 2rem;
        }
        .card-body {
            padding: 0 2rem 2rem 2rem;
        }
        .stButton button {
            padding: 0.8rem 1.5rem !important;
            font-size: 1rem !important;
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
        gap: 2.5rem; /* More gap */
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 3rem; /* Match main padding */
    }
    
    /* Custom info message for initial state */
    .initial-info-card {
        background: var(--apple-surface);
        border-radius: 16px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.03), 0 1px 6px rgba(0, 0, 0, 0.01);
        border: 1px solid var(--apple-gray-2);
        padding: 3rem 2rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 400px; /* Ensure it takes up space */
    }
    .initial-info-card h3 {
        color: var(--apple-gray-5);
        font-weight: 500;
        margin-bottom: 1rem;
        font-size: 1.5rem;
    }
    .initial-info-card p {
        color: var(--apple-gray-5);
        font-size: 1.1rem;
        line-height: 1.6;
        max-width: 80%;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for robust copying to clipboard
# This function is defined and called within the Streamlit component
# to ensure it executes reliably within the iframe, directly triggered by user action.
# It creates a temporary textarea, copies its content, and removes it.
# document.execCommand('copy') is used as it's more widely supported in iframes
# than navigator.clipboard.writeText().
js_copy_function = """
<script>
function copyTextToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed'; // Prevent scrolling to bottom of page
    textarea.style.left = '-9999px'; // Move off-screen
    document.body.appendChild(textarea);
    textarea.focus(); // Focus the textarea
    textarea.select(); // Select its content
    try {
        document.execCommand('copy'); // Execute copy command
    } catch (err) {
        console.error('Copy command failed:', err);
    } finally {
        document.body.removeChild(textarea); // Remove textarea
    }
}
</script>
"""
st.markdown(js_copy_function, unsafe_allow_html=True)

# --- Data Extraction and Email Generation Functions ---
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

# --- UI Layout ---

# Hero Section - Top banner
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">DAZZLE PREMIUM</h1>
    <p class="hero-subtitle">Intelligent Order Email Generator</p>
</div>
""", unsafe_allow_html=True)

# Main Grid Layout
st.markdown('<div class="main-grid">', unsafe_allow_html=True)

# Left Column - Input Card
with st.container(): # Use st.container() for better organization
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
        "", # Label hidden as per Apple design for clean look, placeholder guides
        height=400,
        placeholder="Paste your complete Shopify order export here...\n\nThe email will generate automatically as you paste.",
        key="order_input",
        help="Simply paste the order details and the email will be generated instantly"
    )
    
    # Action Buttons
    col1_btn, col2_btn = st.columns(2)
    with col1_btn:
        high_risk_clicked = st.button("⚠️ High-Risk Email", key="high_risk_btn")
    with col2_btn:
        st.markdown('<div class="secondary-button">', unsafe_allow_html=True)
        new_order_clicked = st.button("✨ New Order", key="new_order_btn")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# Right Column - Output Card
with st.container():
    # Check if raw_text is present or if high_risk_action was triggered
    if raw_text.strip() or (st.session_state.get("email_generated") and not st.session_state.get("reset_clicked")):
        # Simulate processing for a brief moment for a smoother UX
        if raw_text.strip() != st.session_state.last_input:
            st.session_state.processing = True
            st.session_state.email_generated = False # Reset flag
            time.sleep(0.1) # Small delay for visual effect
            st.session_state.processing = False
            st.session_state.last_input = raw_text.strip() # Update last input

        # Process the order data if input is available
        if raw_text.strip():
            order_data = extract_order_data(raw_text)
            missing_info = validate_order_data(order_data)
            
            # Determine email type
            is_high_risk = high_risk_clicked # high_risk_clicked is only True if the button was pressed in this run
            
            email_content = generate_email_content(order_data, is_high_risk)
            subject = f"Final Order Confirmation of dazzlepremium#{order_data['order_number']}"

            # Update session state with generated content
            st.session_state.generated_email_body = email_content
            st.session_state.current_subject = subject
            st.session_state.current_email_address = order_data['email_address']
            st.session_state.current_phone_number = order_data['phone_number']
            st.session_state.email_generated = True

        # Status indicator
        status_html = ""
        if st.session_state.processing:
            status_html = '<div class="status-indicator status-processing"><span class="processing-spinner"></span> Generating...</div>'
        elif high_risk_clicked and raw_text.strip(): # Check high_risk_clicked explicitly for this run
            status_html = '<div class="status-indicator status-warning"><span>⚠️</span> High-Risk Email Generated</div>'
        elif missing_info and raw_text.strip():
            status_html = f'<div class="status-indicator status-warning"><span>⚠️</span> Please verify: {", ".join(missing_info)}</div>'
        elif st.session_state.email_generated and raw_text.strip(): # Only show ready if email was successfully generated
            status_html = '<div class="status-indicator status-ready"><span>✅</span> Email Ready</div>'
        
        st.markdown(f"""
        <div class="card animate-in">
            <div class="card-header">
                <h2 class="card-title">✉️ Generated Email</h2>
                <p class="card-subtitle">Review the details below and copy with a single click.</p>
            </div>
            <div class="card-body">
                {status_html}
        """, unsafe_allow_html=True)
        
        # Email details (using session state for persistence across reruns)
        st.markdown(f"""
        <div class="info-chip">
            <div class="info-chip-label">Email Address</div>
            <div>{st.session_state.current_email_address}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="info-chip">
            <div class="info-chip-label">Subject Line</div>
            <div>{st.session_state.current_subject}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin: 1.5rem 0 0.5rem 0;"><strong>📋 Email Body</strong></div>', unsafe_allow_html=True)
        st.code(st.session_state.generated_email_body, language="text") # Display in a code block for plain text integrity
        
        st.markdown(f"""
        <div class="info-chip">
            <div class="info-chip-label">Phone Number</div>
            <div>{st.session_state.current_phone_number}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Copy to Clipboard Button
        st.markdown("<div style='display: flex; justify-content: center; margin-top: 2rem;'>", unsafe_allow_html=True)
        if st.button("✨ Copy Email to Clipboard", key="copy_email_btn"):
            # Use json.dumps to safely escape the string for JavaScript
            escaped_message = json.dumps(st.session_state.generated_email_body)
            st.components.v1.html(
                f"<script>copyTextToClipboard({escaped_message});</script>",
                height=0, width=0
            )
            st.toast("Email copied to clipboard!", icon="✅") # Apple-like toast notification
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True) # Close card-body and card divs
        
    else:
        # Empty state with helpful guidance
        st.markdown("""
        <div class="initial-info-card animate-in">
            <h3 style="color: var(--apple-gray-5); font-weight: 500;">
                Ready to generate your email?
            </h3>
            <p style="color: var(--apple-gray-5); font-size: 1.1rem; line-height: 1.6;">
                Simply paste your Shopify order export into the input field on the left,<br>
                and your professional email will appear instantly on this side.
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Close main-grid

# Handle new order reset (must be outside the main grid to avoid re-rendering issues)
if new_order_clicked:
    st.session_state.reset_clicked = True
    st.experimental_rerun() # Force a full rerun to clear all state
