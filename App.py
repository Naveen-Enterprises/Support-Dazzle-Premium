import streamlit as st
import re
import json # Import the json module

# --- Page Configuration ---
st.set_page_config(page_title="DAZZLE PREMIUM Order Email Generator", layout="wide", initial_sidebar_state="collapsed")

# --- Custom CSS Styling (Inspired by Material Design & Google Aesthetics) ---
# Using Google Fonts (Inter for body, Montserrat for headings)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@700&display=swap" rel="stylesheet">
<style>
    /* CSS Variables for consistent theming */
    :root {
        --primary-blue: #2F80ED;
        --primary-blue-dark: #1366d6;
        --light-blue-bg: #EEF2F8;
        --text-dark: #1A1A1A;
        --text-medium: #4A4A4A;
        --text-light: #757575;
        --border-color: #D1D5DB;
        --bg-light: #F8F9FA;
        --card-bg: #FFFFFF;

        /* Feedback colors */
        --success-bg: #D4EDDA;
        --success-text: #155724;
        --warning-bg: #FFF3CD;
        --warning-text: #856404;
        --error-bg: #FFCCCC;
        --error-text: #900;

        /* Shadows */
        --shadow-sm: rgba(0, 0, 0, 0.05) 0px 1px 2px 0px;
        --shadow-md: rgba(0, 0, 0, 0.1) 0px 4px 6px -1px, rgba(0, 0, 0, 0.06) 0px 2px 4px -1px;
    }

    /* General Body and App Styling */
    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        color: var(--text-dark);
        background-color: var(--bg-light);
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px; /* Max width for content */
        margin: 0 auto; /* Center content */
    }

    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Montserrat', sans-serif;
        color: var(--primary-blue);
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    h1 { font-size: 2.5rem; text-align: center; margin-bottom: 2rem; }
    h2 { font-size: 2rem; }
    h3 { font-size: 1.5rem; }
    h4 { font-size: 1.2rem; }

    /* Input Fields (Text, Text Area) */
    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        border: 1px solid var(--border-color);
        border-radius: 12px; /* More rounded */
        padding: 0.75rem 1rem;
        font-size: 1rem;
        box-shadow: none;
        transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        background-color: var(--card-bg); /* White background for inputs */
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > textarea:focus {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(47, 128, 237, 0.2); /* Focus ring */
        outline: none;
    }

    /* Buttons */
    .stButton button {
        background-color: var(--primary-blue);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        border-radius: 10px; /* More rounded */
        border: none;
        box-shadow: var(--shadow-sm);
        transition: background-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out, transform 0.1s ease-in-out;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: var(--primary-blue-dark);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    .stButton button:active {
        transform: translateY(0);
        box-shadow: var(--shadow-sm);
    }

    /* Secondary Button Style (for 'Start New Order') */
    /* Streamlit doesn't directly support 'kind' in custom CSS, so we target it by text or position if needed.
       For simplicity, we'll assume a specific button text or order for styling. */
    .stButton button[data-testid="stButton"] { /* Generic target, may need refinement */
        /* This targets all buttons, so specific overrides are needed for primary */
    }

    /* Custom Card Styles for Data Display */
    .info-card, .success-card, .warning-card, .error-card {
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
    }
    .info-card { background-color: var(--light-blue-bg); color: var(--primary-blue); }
    .success-card { background-color: var(--success-bg); color: var(--success-text); }
    .warning-card { background-color: var(--warning-bg); color: var(--warning-text); }
    .error-card { background-color: var(--error-bg); color: var(--error-text); }

    /* Specific Data Display Boxes (Email, Subject, Phone) */
    .data-display-box {
        background-color: var(--light-blue-bg);
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: var(--text-dark);
        font-weight: 500;
        font-size: 1rem;
        word-break: break-all;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        box-shadow: var(--shadow-sm);
    }
    .data-display-box span {
        flex-grow: 1;
    }

    /* Copy Button within Data Display */
    .copy-button {
        background-color: var(--primary-blue);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.2s ease-in-out;
        white-space: nowrap; /* Prevent text wrapping */
    }
    .copy-button:hover {
        background-color: var(--primary-blue-dark);
    }

    /* Extracted Data Review Cards */
    .extracted-data-card {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-md);
    }
    .extracted-data-card h3 {
        margin-top: 0;
        margin-bottom: 1rem;
        color: var(--text-dark);
        font-size: 1.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .extracted-data-card .field-row {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.75rem;
    }
    .extracted-data-card .field-label {
        font-weight: 600;
        color: var(--text-medium);
        min-width: 120px; /* Align labels */
    }
    .extracted-data-card .field-value-display {
        flex-grow: 1;
        font-size: 1rem;
        color: var(--text-dark);
        background-color: var(--light-blue-bg);
        padding: 0.6rem 1rem;
        border-radius: 8px;
        word-break: break-all;
    }
    .extracted-data-card .edit-icon {
        cursor: pointer;
        color: var(--primary-blue);
        opacity: 0.7;
        transition: opacity 0.2s ease-in-out;
    }
    .extracted-data-card .edit-icon:hover {
        opacity: 1;
    }

    /* Order Items List */
    .order-item {
        background-color: var(--light-blue-bg);
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        box-shadow: var(--shadow-sm);
    }
    .order-item strong {
        color: var(--primary-blue);
    }
    .order-item span {
        color: var(--text-dark);
    }
    .order-item .item-detail {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .order-item .item-detail .label {
        font-weight: 600;
        color: var(--text-medium);
        min-width: 80px;
    }
    .order-item .item-detail .value {
        flex-grow: 1;
    }

    /* Code Block Styling */
    .stCode {
        background-color: #f0f2f5; /* Lighter background for code */
        border-radius: 12px;
        padding: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.6;
        white-space: pre-wrap; /* Ensure wrapping */
        word-break: break-all;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
    }

    /* Responsive Adjustments */
    @media (max-width: 768px) {
        h1 { font-size: 2rem; }
        h2 { font-size: 1.7rem; }
        .main .block-container { padding: 1rem; }
        .extracted-data-card .field-row { flex-direction: column; align-items: flex-start; }
        .extracted-data-card .field-label { min-width: auto; margin-bottom: 0.25rem; }
        .data-display-box { flex-direction: column; align-items: flex-start; }
        .copy-button { width: 100%; margin-top: 0.5rem; }
    }
</style>
""", unsafe_allow_html=True)

# --- JavaScript for Copy to Clipboard Functionality ---
# This script is injected once and provides a JS function to copy text.
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
            setTimeout(() => { element.innerText = 'Copy'; }, 1500); // Reset text after 1.5s
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
    st.session_state.current_step = "input"  # input, generate_standard, generate_high_risk
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
    """
    Parses the raw Shopify order export text to extract key information.
    This function uses more robust regex patterns to handle variations.
    """
    data = {
        "customer_name": "[Customer Name Not Found]",
        "email_address": "[Email Not Found]",
        "phone_number": "[Phone Not Found]",
        "order_number": "[Order # Not Found]",
        "items": [],
        "missing_info": []
    }

    lines = [line.strip() for line in raw_text_input.split('\n') if line.strip()]

    # --- Extract Customer Name ---
    # Look for "Customer\n", "Shipping address\n", "Billing address\n" followed by a name line
    name_found = False
    for i, line in enumerate(lines):
        if re.search(r"Customer\s*$", line, re.IGNORECASE) and i + 1 < len(lines):
            data["customer_name"] = lines[i+1].split('\n')[0].strip()
            name_found = True
            break
        elif re.search(r"Shipping address\s*$", line, re.IGNORECASE) and i + 1 < len(lines):
            data["customer_name"] = lines[i+1].split('\n')[0].strip()
            name_found = True
            break
        elif re.search(r"Billing address\s*$", line, re.IGNORECASE) and i + 1 < len(lines):
            data["customer_name"] = lines[i+1].split('\n')[0].strip()
            name_found = True
            break
    if not name_found:
        data["missing_info"].append("Customer Name")

    # --- Extract Email Address ---
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.[\w\.-]+", raw_text_input)
    if email_match:
        data["email_address"] = email_match.group(0).strip()
    else:
        data["missing_info"].append("Email Address")

    # --- Extract Phone Number ---
    # More flexible phone number regex for common US formats
    phone_match = re.search(r"(\+1[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4}|\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4})", raw_text_input)
    if phone_match:
        data["phone_number"] = phone_match.group(0).strip()
    else:
        data["missing_info"].append("Phone Number")

    # --- Extract Order Number ---
    order_number_match = re.search(r"dazzlepremium#(\d+)", raw_text_input, re.IGNORECASE)
    if order_number_match:
        data["order_number"] = order_number_match.group(1).strip()
    else:
        data["missing_info"].append("Order Number")

    # --- Extract Items ---
    # This is the trickiest part, relies on specific patterns in Shopify export.
    # We look for lines that look like product names, then try to find size/SKU below them.
    
    # A list to hold the raw product lines and their potential indices
    product_lines_info = []
    for i, line in enumerate(lines):
        # Heuristic: A line containing " - " and a potential SKU-like pattern
        # and not explicitly a SKU or Discount line itself
        if " - " in line and re.search(r" - [A-Z0-9\-]+$", line) and \
           not any(kw in line.lower() for kw in ["sku", "discount", "subtotal", "shipping", "tax", "total"]):
            product_lines_info.append({"line": line, "index": i})

    for prod_info in product_lines_info:
        product_line = prod_info["line"]
        line_idx = prod_info["index"]
        
        product_name, style_code = product_line.rsplit(" - ", 1)
        size = "[Size Not Found]"
        
        # Look for size/quantity in the next few lines
        for offset in range(1, 5): # Check up to 4 lines after product line
            if line_idx + offset < len(lines):
                potential_size_line = lines[line_idx + offset]
                
                # Heuristic for size line:
                # - Contains common size patterns (e.g., "M", "XL", "32", "32/30", "US 10")
                # - Not a price or SKU line
                if re.match(r"^((\d{1,2}(/\d{1,2})?[\s/]?[A-Z]{2,3})|[XSML]{1,3}|[0-9]{1,2}|US\s*\d{1,2}|EU\s*\d{1,2})\b", potential_size_line, re.IGNORECASE) and \
                   not potential_size_line.startswith("$") and not "SKU" in potential_size_line.upper():
                    size = potential_size_line.split('\n')[0].strip().split(' ')[0] # Take the first part of the size line
                    break
        
        data["items"].append({
            "product_name": product_name.strip(),
            "style_code": style_code.strip(),
            "size": size
        })
        
        if "[Size Not Found]" in size:
            if "Item Sizes" not in data["missing_info"]:
                data["missing_info"].append("Item Sizes")


    if not data["items"]:
        data["missing_info"].append("Order Items")

    return data


def generate_standard_email(parsed_data):
    """Generates the standard order confirmation email."""
    customer_name = parsed_data.get("customer_name", "[Customer Name Not Found]")
    order_number = parsed_data.get("order_number", "[Order # Not Found]")
    items = parsed_data.get("items", [])

    order_details_list = []
    for idx, item in enumerate(items):
        order_details_list.append(
            f"- Item {idx+1}:\n•\u2060  \u2060Product: {item.get('product_name', 'N/A')}\n"
            f"•\u2060  \u2060Style Code: {item.get('style_code', 'N/A')}\n"
            f"•\u2060  \u2060Size: {item.get('size', 'N/A')}"
        )
    order_details = "\n\n".join(order_details_list) if order_details_list else "No items found."

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

    return subject, message

def generate_high_risk_email(parsed_data):
    """Generates the high-risk order cancellation email."""
    customer_name = parsed_data.get("customer_name", "[Customer Name Not Found]")

    subject = f"Important: Your DAZZLE PREMIUM Order - Action Required"
    message = f"""Hello {customer_name},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we’d be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email.

Thank you,
DAZZLE PREMIUM Support"""
    return subject, message


def reset_app_state():
    """Resets all session state variables to their initial values."""
    st.session_state.current_step = "input"
    st.session_state.raw_text = ""
    st.session_state.parsed_data = {}
    st.session_state.generated_email_body = ""
    st.session_state.generated_subject = ""
    st.session_state.missing_info_flags = []
    # No st.rerun() here, as it's called by the button's on_click directly.
    # We need to ensure the state is cleared before the next render cycle.
    # The button's on_click will trigger a rerun.

# --- Main Application Logic ---

st.markdown("""<h1 style='text-align: center;'>📦 DAZZLE PREMIUM Order Email Generator</h1>""", unsafe_allow_html=True)

# Create two columns for the main layout
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("1. Paste Shopify Order Export")
    st.markdown("""
        <div class="info-card">
            <span style="font-size: 1.5rem;">📄</span>
            Paste the full text from your Shopify order export summary below.
            We'll automatically extract all the necessary details.
        </div>
    """, unsafe_allow_html=True)

    raw_text_input = st.text_area(
        "Full Order Export Text",
        height=400,
        value=st.session_state.raw_text,
        placeholder="Paste your Shopify order details here...",
        key="raw_text_input_main" # Add a key to avoid potential conflicts
    )

    col_buttons_input = st.columns(2)
    with col_buttons_input[0]:
        if st.button("✨ Generate Email", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                st.session_state.parsed_data = parse_shopify_export(raw_text_input)
                st.session_state.missing_info_flags = st.session_state.parsed_data["missing_info"]
                
                subject, message = generate_standard_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_standard" # Keep track of which email type was generated
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate an email.")
    with col_buttons_input[1]:
        if st.button("🚨 High-Risk Order Email", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                st.session_state.parsed_data = parse_shopify_export(raw_text_input)
                subject, message = generate_high_risk_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_high_risk" # Keep track of which email type was generated
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate a high-risk email.")

with col_right:
    st.subheader("2. Your Generated Email")
    
    # Conditionally display content based on whether an email has been generated
    if st.session_state.generated_email_body:
        if st.session_state.current_step == "generate_standard":
            if st.session_state.missing_info_flags:
                st.markdown(f"""
                    <div class="warning-card">
                        <span style="font-size: 1.5rem;">⚠️</span>
                        We couldn't find all the information automatically. Please double-check the following fields in the email: <strong>{', '.join(st.session_state.missing_info_flags)}</strong>.
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="success-card">
                        <span style="font-size: 1.5rem;">✅</span>
                        All information looks good! Ready to copy and send.
                    </div>
                """, unsafe_allow_html=True)

            # Display standard email details
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
            
            # Fix applied here: Use json.dumps to safely embed the email body into JavaScript
            js_safe_email_body = json.dumps(st.session_state.generated_email_body)
            st.markdown(f"""
                <div style="text-align: right; margin-top: -1.5rem; margin-bottom: 1.5rem;">
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<h4>📱 Customer Phone Number:</h4>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="data-display-box">
                    <span>{st.session_state.parsed_data.get('phone_number', 'N/A')}</span>
                    <button class="copy-button" id="copyPhoneBtn" onclick="copyToClipboard(
                        '{st.session_state.parsed_data.get('phone_number', 'N/A').replace("'", "\\'")}', 'copyPhoneBtn'
                    )">Copy</button>
                </div>
            """, unsafe_allow_html=True)

        elif st.session_state.current_step == "generate_high_risk":
            st.markdown("""
                <div class="warning-card">
                    <span style="font-size: 1.5rem;">🚨</span>
                    This is the email for high-risk order cancellations. Please review carefully before sending.
                </div>
            """, unsafe_allow_html=True)

            # Display high-risk email details
            st.markdown("<h4>📨 Subject:</h4>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="data-display-box">
                    <span>{st.session_state.generated_subject}</span>
                    <button class="copy-button" id="copyHRSubjectBtn" onclick="copyToClipboard(
                        '{st.session_state.generated_subject.replace("'", "\\'")}', 'copyHRSubjectBtn'
                    )">Copy</button>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<h4>📝 Email Body:</h4>", unsafe_allow_html=True)
            st.code(st.session_state.generated_email_body, language="text")

            # Fix applied here for high-risk email as well
            js_safe_email_body_hr = json.dumps(st.session_state.generated_email_body)
            st.markdown(f"""
                <div style="text-align: right; margin-top: -1.5rem; margin-bottom: 1.5rem;">
                    <button class="copy-button" id="copyHRBodyBtn" onclick="copyToClipboard(
                        {js_safe_email_body_hr}, 'copyHRBodyBtn'
                    )">Copy Email Body</button>
                </div>
            """, unsafe_allow_html=True)
        
        # Always show "Start New Order" button on the right side if an email has been generated
        st.button("🔁 Start New Order", on_click=reset_app_state, use_container_width=True)
    else:
        # Placeholder message when no email has been generated yet
        st.markdown("""
            <div class="info-card" style="min-height: 500px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                <span style="font-size: 3rem; margin-bottom: 1rem;">✨</span>
                <p style="font-size: 1.2rem; font-weight: 600;">Your generated email will appear here.</p>
                <p style="color: var(--text-medium);">Paste your order details on the left and click 'Generate Email' to see the magic!</p>
            </div>
        """, unsafe_allow_html=True)
