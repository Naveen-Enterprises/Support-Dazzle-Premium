import streamlit as st
import re
import json # Import the json module
import asyncio # For async operations with LLM
import httpx # For making async HTTP requests

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
    st.session_state.current_step = "input"  # input, generate_standard, generate_high_risk, generate_return
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = {}
if "generated_email_body" not in st.session_state:
    st.session_state.generated_email_body = ""
if "generated_subject" not in st.session_state:
    st.session_state.generated_subject = ""
# Removed missing_info_flags as LLM will provide defaults

# --- Helper Functions ---

async def parse_shopify_export_with_llm(raw_text_input):
    """
    Parses the raw Shopify order export text using an LLM to extract key information
    and return it in a structured JSON format.
    """
    api_key = "" # If you want to use models other than gemini-2.0-flash, provide an API key here.
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    # Define the JSON schema for the LLM's response
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "customer_name": { "type": "STRING", "default": "Customer" },
            "email_address": { "type": "STRING", "default": "email@example.com" },
            "phone_number": { "type": "STRING", "default": "N/A" },
            "order_number": { "type": "STRING", "default": "UNKNOWN" },
            "items": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "product_name": { "type": "STRING", "default": "Unknown Product" },
                        "style_code": { "type": "STRING", "default": "N/A" },
                        "size": { "type": "STRING", "default": "N/A" },
                        "quantity": { "type": "INTEGER", "default": 1 }
                    },
                    "required": ["product_name", "style_code", "size", "quantity"]
                }
            }
        },
        "required": ["customer_name", "email_address", "phone_number", "order_number", "items"]
    }

    prompt = f"""You are an expert data extractor. Your task is to extract specific information from the provided Shopify order export text and return it in a strict JSON format.
    If a piece of information is not found, use the default placeholder specified in the schema.
    Ensure all fields are present in the JSON output, using defaults if necessary.

    Shopify Order Export Text:
    ---
    {raw_text_input}
    ---
    """

    chat_history = []
    chat_history.append({ "role": "user", "parts": [{ "text": prompt }] })

    payload = {
        "contents": chat_history,
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=payload, timeout=60.0) # Increased timeout
            response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
            result = response.json()

        if result.get("candidates") and result["candidates"][0].get("content") and result["candidates"][0]["content"].get("parts"):
            json_text = result["candidates"][0]["content"]["parts"][0]["text"]
            parsed_data = json.loads(json_text)
            return parsed_data
        else:
            st.error("LLM did not return a valid response structure.")
            return {
                "customer_name": "Customer",
                "email_address": "email@example.com",
                "phone_number": "N/A",
                "order_number": "UNKNOWN",
                "items": []
            }
    except httpx.RequestError as e:
        st.error(f"Network or API request error: {e}")
        return {
            "customer_name": "Customer",
            "email_address": "email@example.com",
            "phone_number": "N/A",
            "order_number": "UNKNOWN",
            "items": []
        }
    except json.JSONDecodeError as e:
        st.error(f"Failed to decode JSON from LLM response: {e}. Raw response: {json_text}")
        return {
            "customer_name": "Customer",
            "email_address": "email@example.com",
            "phone_number": "N/A",
            "order_number": "UNKNOWN",
            "items": []
        }
    except Exception as e:
        st.error(f"An unexpected error occurred during LLM parsing: {e}")
        return {
            "customer_name": "Customer",
            "email_address": "email@example.com",
            "phone_number": "N/A",
            "order_number": "UNKNOWN",
            "items": []
        }

def generate_standard_email(parsed_data):
    """Generates the standard order confirmation email."""
    customer_name = parsed_data.get("customer_name", "Customer")
    order_number = parsed_data.get("order_number", "UNKNOWN")
    items = parsed_data.get("items", [])

    order_details_list = []
    for idx, item in enumerate(items):
        order_details_list.append(
            f"- Item {idx+1}:\n•\u2060  \u2060Product: {item.get('product_name', 'N/A')}\n"
            f"•\u2060  \u2060Style Code: {item.get('style_code', 'N/A')}\n"
            f"•\u2060  \u2060Size: {item.get('size', 'N/A')}\n"
            f"•\u2060  \u2060Quantity: {item.get('quantity', 1)}" # Added quantity
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
    customer_name = parsed_data.get("customer_name", "Customer")

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

def generate_return_email(parsed_data):
    """Generates the return mail template."""
    customer_name = parsed_data.get("customer_name", "Customer") # Get the customer name

    subject = f"DAZZLE PREMIUM: Your Return Request Instructions"
    message = f"""Dear {customer_name},
Thank you for reaching out to us regarding your return request. To 
ensure a smooth and successful return process, please carefully follow 
the steps below:
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

Once we receive the returned item in its original condition with the 
tags intact and complete our inspection, we will process your refund.
If you have any questions, feel free to reply to this email.
"""
    return subject, message


def reset_app_state():
    """Resets all session state variables to their initial values."""
    st.session_state.current_step = "input"
    st.session_state.raw_text = ""
    st.session_state.parsed_data = {}
    st.session_state.generated_email_body = ""
    st.session_state.generated_subject = ""
    st.rerun() # Rerun to clear the UI immediately

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

    col_buttons_input = st.columns(3) # Changed to 3 columns for 3 buttons
    with col_buttons_input[0]:
        if st.button("✨ Generate Order Email", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                with st.spinner("Extracting details and generating email..."):
                    st.session_state.parsed_data = asyncio.run(parse_shopify_export_with_llm(raw_text_input))
                
                subject, message = generate_standard_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_standard" # Keep track of which email type was generated
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate an email.")
    with col_buttons_input[1]:
        if st.button("🚨 High-Risk Email", use_container_width=True): # Shorter button text
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                with st.spinner("Extracting details and generating high-risk email..."):
                    st.session_state.parsed_data = asyncio.run(parse_shopify_export_with_llm(raw_text_input))
                
                subject, message = generate_high_risk_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_high_risk" # Keep track of which email type was generated
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate a high-risk email.")
    with col_buttons_input[2]: # New button for return email
        if st.button("↩️ Return Email Template", use_container_width=True):
            if raw_text_input:
                st.session_state.raw_text = raw_text_input
                with st.spinner("Extracting details and generating return email..."):
                    st.session_state.parsed_data = asyncio.run(parse_shopify_export_with_llm(raw_text_input)) # Parse to get customer name
                
                subject, message = generate_return_email(st.session_state.parsed_data)
                st.session_state.generated_subject = subject
                st.session_state.generated_email_body = message
                st.session_state.current_step = "generate_return"
                st.rerun()
            else:
                st.warning("Please paste the order export text to generate a return email.")


with col_right:
    st.subheader("2. Your Generated Email")
    
    # Conditionally display content based on whether an email has been generated
    if st.session_state.generated_email_body:
        # Display a generic success message since LLM handles defaults
        st.markdown("""
            <div class="success-card">
                <span style="font-size: 1.5rem;">✅</span>
                Email generated successfully! Ready to copy and send.
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.current_step == "generate_standard":
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
                    <button class="copy-button" id="copyBodyBtn" onclick="copyToClipboard(
                        {js_safe_email_body}, 'copyBodyBtn'
                    )">Copy Email Body</button>
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
            
        elif st.session_state.current_step == "generate_return":
            st.markdown("""
                <div class="info-card">
                    <span style="font-size: 1.5rem;">↩️</span>
                    This is the return mail template. Ensure the customer name is correct.
                </div>
            """, unsafe_allow_html=True)

            # Display return email details
            st.markdown("<h4>📧 Recipient Email:</h4>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="data-display-box">
                    <span>{st.session_state.parsed_data.get('email_address', 'N/A')}</span>
                    <button class="copy-button" id="copyReturnEmailBtn" onclick="copyToClipboard(
                        '{st.session_state.parsed_data.get('email_address', 'N/A').replace("'", "\\'")}', 'copyReturnEmailBtn'
                    )">Copy</button>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<h4>📨 Subject:</h4>", unsafe_allow_html=True)
            st.markdown(f"""
                <div class="data-display-box">
                    <span>{st.session_state.generated_subject}</span>
                    <button class="copy-button" id="copyReturnSubjectBtn" onclick="copyToClipboard(
                        '{st.session_state.generated_subject.replace("'", "\\'")}', 'copyReturnSubjectBtn'
                    )">Copy</button>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<h4>📝 Email Body:</h4>", unsafe_allow_html=True)
            st.code(st.session_state.generated_email_body, language="text")

            js_safe_email_body_return = json.dumps(st.session_state.generated_email_body)
            st.markdown(f"""
                <div style="text-align: right; margin-top: -1.5rem; margin-bottom: 1.5rem;">
                    <button class="copy-button" id="copyReturnBodyBtn" onclick="copyToClipboard(
                        {js_safe_email_body_return}, 'copyReturnBodyBtn'
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

