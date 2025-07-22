import streamlit as st
import re
import json
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Order Email Generator", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "email_generated" not in st.session_state:
    st.session_state.email_generated = False
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "processing" not in st.session_state:
    st.session_state.processing = False
if "generated_email_body" not in st.session_state:
    st.session_state.generated_email_body = ""
if "current_subject" not in st.session_state:
    st.session_state.current_subject = ""
if "current_email_address" not in st.session_state:
    st.session_state.current_email_address = ""
if "current_phone_number" not in st.session_state:
    st.session_state.current_phone_number = ""
if "is_high_risk" not in st.session_state:
    st.session_state.is_high_risk = False

# --- Claude-Inspired Design System ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --claude-bg: #fafaf9;
        --claude-surface: #ffffff;
        --claude-border: #e5e7eb;
        --claude-border-light: #f3f4f6;
        --claude-text-primary: #111827;
        --claude-text-secondary: #6b7280;
        --claude-text-muted: #9ca3af;
        --claude-accent: #2563eb;
        --claude-accent-hover: #1d4ed8;
        --claude-success: #10b981;
        --claude-warning: #f59e0b;
        --claude-error: #ef4444;
        --claude-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
        --claude-shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    }
    
    * {
        box-sizing: border-box;
    }
    
    .stApp {
        background: var(--claude-bg);
    }
    
    /* Hide Streamlit elements */
    .stDeployButton, footer, header, .stDecoration {
        display: none !important;
    }
    
    /* Main container */
    .main .block-container {
        padding: 0 !important;
        max-width: none !important;
        height: 100vh;
        overflow: hidden;
    }
    
    /* Split screen layout */
    .split-container {
        display: flex;
        height: 100vh;
        width: 100vw;
    }
    
    .left-panel, .right-panel {
        flex: 1;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    }
    
    .left-panel {
        background: var(--claude-surface);
        border-right: 1px solid var(--claude-border);
    }
    
    .right-panel {
        background: var(--claude-bg);
    }
    
    /* Header styles */
    .panel-header {
        padding: 24px 32px 16px 32px;
        border-bottom: 1px solid var(--claude-border-light);
        background: var(--claude-surface);
    }
    
    .right-panel .panel-header {
        background: var(--claude-bg);
        border-bottom: 1px solid var(--claude-border);
    }
    
    .panel-title {
        font-family: 'Inter', sans-serif;
        font-size: 20px;
        font-weight: 600;
        color: var(--claude-text-primary);
        margin: 0 0 4px 0;
        line-height: 1.2;
    }
    
    .panel-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: var(--claude-text-secondary);
        margin: 0;
        line-height: 1.4;
    }
    
    /* Content areas */
    .panel-content {
        flex: 1;
        overflow-y: auto;
        padding: 24px 32px;
    }
    
    /* Text area styling */
    .stTextArea > div > div > textarea {
        font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        padding: 16px !important;
        border: 1px solid var(--claude-border) !important;
        border-radius: 8px !important;
        background: var(--claude-surface) !important;
        color: var(--claude-text-primary) !important;
        resize: none !important;
        height: calc(100vh - 200px) !important;
        min-height: calc(100vh - 200px) !important;
        box-shadow: var(--claude-shadow) !important;
        transition: border-color 0.15s ease !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--claude-accent) !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgb(37 99 235 / 0.1) !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: var(--claude-text-muted) !important;
        font-style: normal !important;
    }
    
    /* Button styles */
    .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 8px 16px !important;
        border-radius: 6px !important;
        border: 1px solid var(--claude-border) !important;
        background: var(--claude-surface) !important;
        color: var(--claude-text-primary) !important;
        transition: all 0.15s ease !important;
        box-shadow: var(--claude-shadow) !important;
        height: 36px !important;
        min-height: 36px !important;
    }
    
    .stButton > button:hover {
        background: var(--claude-bg) !important;
        border-color: var(--claude-text-muted) !important;
    }
    
    .primary-button > button {
        background: var(--claude-accent) !important;
        color: white !important;
        border-color: var(--claude-accent) !important;
    }
    
    .primary-button > button:hover {
        background: var(--claude-accent-hover) !important;
        border-color: var(--claude-accent-hover) !important;
    }
    
    .danger-button > button {
        background: var(--claude-error) !important;
        color: white !important;
        border-color: var(--claude-error) !important;
    }
    
    .danger-button > button:hover {
        background: #dc2626 !important;
        border-color: #dc2626 !important;
    }
    
    /* Button container */
    .button-row {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
    }
    
    .button-row .stButton {
        flex: 1;
    }
    
    /* Status indicator */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
    }
    
    .status-ready {
        background: rgba(16, 185, 129, 0.1);
        color: var(--claude-success);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.1);
        color: var(--claude-warning);
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .status-processing {
        background: rgba(37, 99, 235, 0.1);
        color: var(--claude-accent);
        border: 1px solid rgba(37, 99, 235, 0.2);
    }
    
    /* Info sections */
    .info-section {
        margin-bottom: 24px;
    }
    
    .info-label {
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 500;
        color: var(--claude-text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    
    .info-value {
        font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
        font-size: 14px;
        color: var(--claude-text-primary);
        background: var(--claude-surface);
        padding: 12px 16px;
        border: 1px solid var(--claude-border);
        border-radius: 6px;
        word-break: break-all;
    }
    
    .email-body {
        font-family: 'SF Mono', 'Monaco', 'Cascadia Code', monospace;
        font-size: 13px;
        line-height: 1.6;
        color: var(--claude-text-primary);
        background: var(--claude-surface);
        padding: 20px;
        border: 1px solid var(--claude-border);
        border-radius: 8px;
        white-space: pre-wrap;
        word-wrap: break-word;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: var(--claude-shadow);
    }
    
    /* Empty state */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100%;
        text-align: center;
        color: var(--claude-text-muted);
    }
    
    .empty-state-icon {
        font-size: 48px;
        margin-bottom: 16px;
        opacity: 0.5;
    }
    
    .empty-state-title {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        font-weight: 500;
        margin-bottom: 8px;
        color: var(--claude-text-secondary);
    }
    
    .empty-state-text {
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: var(--claude-text-muted);
        max-width: 300px;
        line-height: 1.5;
    }
    
    /* Spinner */
    .spinner {
        width: 14px;
        height: 14px;
        border: 2px solid var(--claude-accent);
        border-top: 2px solid transparent;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Copy button */
    .copy-button-container {
        margin-top: 20px;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .split-container {
            flex-direction: column;
        }
        
        .left-panel, .right-panel {
            flex: none;
            height: 50vh;
        }
        
        .panel-content {
            padding: 16px 20px;
        }
        
        .panel-header {
            padding: 16px 20px 12px 20px;
        }
        
        .stTextArea > div > div > textarea {
            height: calc(50vh - 150px) !important;
            min-height: calc(50vh - 150px) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# JavaScript for copying to clipboard
js_copy_function = """
<script>
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.left = '-999999px';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();
    try {
        document.execCommand('copy');
        return true;
    } catch (err) {
        console.error('Copy failed:', err);
        return false;
    } finally {
        document.body.removeChild(textarea);
    }
}
</script>
"""
st.markdown(js_copy_function, unsafe_allow_html=True)

# --- Data Processing Functions ---
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

# --- Main Layout ---
st.markdown('<div class="split-container">', unsafe_allow_html=True)

# Left Panel - Input
st.markdown('''
<div class="left-panel">
    <div class="panel-header">
        <h1 class="panel-title">Order Input</h1>
        <p class="panel-subtitle">Paste your Shopify order export below</p>
    </div>
    <div class="panel-content">
''', unsafe_allow_html=True)

# Button row
st.markdown('<div class="button-row">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="primary-button">', unsafe_allow_html=True)
    generate_clicked = st.button("Generate Email", key="generate_btn")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="danger-button">', unsafe_allow_html=True)
    high_risk_clicked = st.button("High-Risk Email", key="high_risk_btn")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    clear_clicked = st.button("Clear", key="clear_btn")

st.markdown('</div>', unsafe_allow_html=True)

# Text input
raw_text = st.text_area(
    "", 
    placeholder="Paste your complete Shopify order export here...\n\nInclude all order details, customer information, and product details for accurate email generation.",
    key="order_input",
    label_visibility="collapsed"
)

st.markdown('''
    </div>
</div>
''', unsafe_allow_html=True)

# Right Panel - Output
st.markdown('''
<div class="right-panel">
    <div class="panel-header">
        <h1 class="panel-title">Generated Email</h1>
        <p class="panel-subtitle">Review and copy your professional order confirmation</p>
    </div>
    <div class="panel-content">
''', unsafe_allow_html=True)

# Handle button clicks
if clear_clicked:
    st.session_state.email_generated = False
    st.session_state.last_input = ""
    st.session_state.generated_email_body = ""
    st.session_state.current_subject = ""
    st.session_state.current_email_address = ""
    st.session_state.current_phone_number = ""
    st.session_state.is_high_risk = False
    st.rerun()

if (generate_clicked or high_risk_clicked) and raw_text.strip():
    # Process the order
    order_data = extract_order_data(raw_text)
    missing_info = validate_order_data(order_data)
    
    st.session_state.is_high_risk = high_risk_clicked
    email_content = generate_email_content(order_data, high_risk_clicked)
    subject = f"Final Order Confirmation of dazzlepremium#{order_data['order_number']}"
    
    # Update session state
    st.session_state.generated_email_body = email_content
    st.session_state.current_subject = subject
    st.session_state.current_email_address = order_data['email_address']
    st.session_state.current_phone_number = order_data['phone_number']
    st.session_state.email_generated = True

# Display output
if st.session_state.email_generated and st.session_state.generated_email_body:
    # Status badge
    if st.session_state.is_high_risk:
        st.markdown('<div class="status-badge status-warning">⚠️ High-Risk Email Generated</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-badge status-ready">✅ Email Ready</div>', unsafe_allow_html=True)
    
    # Email details
    st.markdown(f'''
    <div class="info-section">
        <div class="info-label">To</div>
        <div class="info-value">{st.session_state.current_email_address}</div>
    </div>
    
    <div class="info-section">
        <div class="info-label">Subject</div>
        <div class="info-value">{st.session_state.current_subject}</div>
    </div>
    
    <div class="info-section">
        <div class="info-label">Phone</div>
        <div class="info-value">{st.session_state.current_phone_number}</div>
    </div>
    
    <div class="info-section">
        <div class="info-label">Email Body</div>
        <div class="email-body">{st.session_state.generated_email_body}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Copy button
    st.markdown('<div class="copy-button-container">', unsafe_allow_html=True)
    st.markdown('<div class="primary-button">', unsafe_allow_html=True)
    if st.button("Copy Email to Clipboard", key="copy_btn"):
        escaped_email = json.dumps(st.session_state.generated_email_body)
        st.components.v1.html(
            f"<script>copyToClipboard({escaped_email});</script>",
            height=0
        )
        st.success("Email copied to clipboard!")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # Empty state
    st.markdown('''
    <div class="empty-state">
        <div class="empty-state-icon">✉️</div>
        <div class="empty-state-title">No email generated yet</div>
        <div class="empty-state-text">Paste your order data on the left and click "Generate Email" to create your professional order confirmation.</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown('''
    </div>
</div>
</div>
''', unsafe_allow_html=True)
