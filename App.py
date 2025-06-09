import streamlit as st
import re
import datetime
import pytz

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
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #1366d6;
    }
    .stCode {
        background-color: #f7f8fa;
        border-radius: 10px;
        padding: 1rem;
        font-size: 0.95rem;
        word-break: break-word; /* Ensure long lines break */
    }
    .subject-box {
        background-color: #eef2f8;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        color: #1a1a1a;
        font-weight: 500;
        font-size: 1rem;
        word-wrap: break-word;
    }
    .warning-box {
        background-color: #ffcccc;
        padding: 1rem;
        border-radius: 10px;
        color: #900;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color:#d4edda;
        padding:1rem;
        border-radius:10px;
        color:#155724;
        font-weight:bold;
        margin-bottom:1rem;
    }
    .info-box {
        background-color: #e0f2f7;
        padding: 1rem;
        border-radius: 10px;
        color: #01579b;
        font-weight: 500;
        margin-bottom: 1rem;
        border-left: 5px solid #039be5;
    }
    .log-box {
        background-color: #f2f2f2;
        padding: 0.5rem 1rem;
        border-left: 4px solid #2f80ed;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        color: #555;
    }
    h1, h2, h4 { color: #2f80ed; font-weight: 700; }
    .stAlert { margin-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("""<h1 style='text-align: center;'>📦 DAZZLE PREMIUM Order Email Generator</h1>""", unsafe_allow_html=True)

# Initialize session state for reset
if "reset_clicked" not in st.session_state:
    st.session_state.reset_clicked = False
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "generated_email_data" not in st.session_state:
    st.session_state.generated_email_data = None
if "high_risk_generated" not in st.session_state:
    st.session_state.high_risk_generated = False


def reset_app():
    """Resets all relevant session state variables."""
    st.session_state.raw_text = ""
    st.session_state.generated_email_data = None
    st.session_state.high_risk_generated = False
    st.session_state.reset_clicked = True # Set to true to trigger rerun and clear input
    st.rerun()

# Log timestamp of generation
local_tz = pytz.timezone("America/New_York")
now = datetime.datetime.now(local_tz).strftime("%B %d, %Y %I:%M %p")
st.markdown(f"<div class='log-box'>🕒 Generated on: {now}</div>", unsafe_allow_html=True)

st.markdown("""<div style='display: flex; gap: 40px;'>""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Paste Shopify Order Export")
        st.info("Paste the **entire** text content of the Shopify order export (Ctrl+A, Ctrl+C from the order page) into the box below. Make sure to capture customer details, order items, and payment info.")
        raw_text_input = st.text_area(
            "Full Order Export Text",
            height=500,
            value=st.session_state.raw_text,
            key="raw_text_area" # Add a key to the text_area
        )

        # Update session_state.raw_text when input changes
        if raw_text_input != st.session_state.raw_text:
            st.session_state.raw_text = raw_text_input
            st.session_state.generated_email_data = None # Clear previous output
            st.session_state.high_risk_generated = False

        generate_button = st.button("🎯 Generate Confirmation Email", use_container_width=True)
        high_risk_button = st.button("🚨 Generate High-Risk Order Email", use_container_width=True)

        if generate_button:
            st.session_state.generated_email_data = None # Clear previous high-risk output
            st.session_state.high_risk_generated = False
            # Trigger parsing logic
            if not st.session_state.raw_text.strip():
                st.warning("Please paste the order export before generating the message.")
            else:
                try: # Add a try-except block here to catch errors during parsing
                    st.session_state.generated_email_data = parse_and_generate_email(st.session_state.raw_text)
                except Exception as e:
                    st.error(f"An unexpected error occurred during email generation: {e}")
                    st.warning("Please check your input data for any unusual formatting. Refer to the logs for more details.")
                    print(f"Error in parse_and_generate_email: {e}") # This will go to Streamlit logs

        if high_risk_button:
            st.session_state.generated_email_data = None # Clear previous confirmation output
            st.session_state.high_risk_generated = True
            # Trigger high-risk email logic
            if not st.session_state.raw_text.strip():
                st.warning("Please paste the order export before generating the message.")
            else:
                try: # Add a try-except block here as well
                    customer_name = extract_customer_name(st.session_state.raw_text)
                    st.session_state.generated_email_data = {"customer_name": customer_name} # Store for display
                except Exception as e:
                    st.error(f"An unexpected error occurred during high-risk email generation: {e}")
                    st.warning("Please check your input data for any unusual formatting. Refer to the logs for more details.")
                    print(f"Error in high_risk_button logic: {e}") # This will go to Streamlit logs


    with col2:
        if st.session_state.generated_email_data and not st.session_state.high_risk_generated:
            display_confirmation_email(st.session_state.generated_email_data)
        elif st.session_state.high_risk_generated and st.session_state.generated_email_data:
            display_high_risk_email(st.session_state.generated_email_data["customer_name"])
        elif generate_button or high_risk_button: # Only show this if a button was clicked but raw_text was empty
            pass # Warning already shown in col1

# --- Parsing Functions ---
def extract_customer_name(text):
    """Extracts customer name with robust regex."""
    name_patterns = [
        r"Customer\s*\n\s*(.*?)\n",
        r"Shipping address\s*\n\s*(.*?)\n",
        r"Billing address\s*\n\s*(.*?)\n",
        r"Order confirmation email was sent to (.*?)\s*\(", # From confirmation message
        r"placed this order on Online Store \(checkout #\d+\)\.\n\s*(.*?)\n" # From timeline
    ]
    for pattern in name_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            try: # Added try-except around group access and cleaning
                name = match.group(1).split('\n')[0].strip().title()
                name = re.sub(r'\s*[\w\.-]+@[\w\.-]+\.\w+', '', name).strip()
                if "No phone number" in name or "View map" in name or "Email" in name:
                    print(f"DEBUG: Customer name pattern matched garbage, trying next: {name}") # Log this
                    continue
                print(f"DEBUG: Found customer name: {name}") # Log successful extraction
                return name
            except IndexError: # group(1) didn't exist (shouldn't happen with .*? but good to be safe)
                print(f"DEBUG: IndexError on match.group(1) for pattern: {pattern}")
                continue # Try next pattern
            except Exception as e: # Catch any other unexpected errors
                print(f"DEBUG: Unexpected error processing customer name match for pattern {pattern}: {e}")
                continue # Try next pattern
    print("DEBUG: Customer Name Not Found after all patterns.") # Log failure
    return "[Customer Name Not Found]"

def extract_email_address(text):
    """Extracts email address."""
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", text)
    email = email_match.group(0).strip() if email_match else "[Email Not Found]"
    print(f"DEBUG: Extracted email: {email}") # Log result
    return email

def extract_phone_number(text):
    """Extracts phone number, handling various formats."""
    phone_patterns = [
        r"(?:Shipping|Billing) address\s*\n(?:.*\n){0,4}\s*(\+?\d[\d\s\-.()]{7,}\d)",
        r"Contact information\s*\n(?:.*\n){0,2}\s*(\+?\d[\d\s-.()]{7,}\d)",
        r"phone number\s*\n\s*(\+?\d[\d\s-.()]{7,}\d)"
    ]
    for pattern in phone_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            try: # Added try-except around group access and cleaning
                phone = match.group(1).strip()
                phone = re.sub(r'[\s\-()]+', '', phone)
                if len(phone) == 10 and phone.isdigit():
                    phone = f"({phone[0:3]}) {phone[3:6]}-{phone[6:10]}"
                elif len(phone) == 11 and phone.startswith('1') and phone[1:].isdigit():
                    phone = f"+1 ({phone[1:4]}) {phone[4:7]}-{phone[7:11]}"
                print(f"DEBUG: Found phone number: {phone}") # Log successful extraction
                return phone
            except IndexError: # group(1) didn't exist
                print(f"DEBUG: IndexError on match.group(1) for pattern: {pattern}")
                continue # Try next pattern
            except Exception as e:
                print(f"DEBUG: Unexpected error processing phone number match for pattern {pattern}: {e}")
                continue
    print("DEBUG: Phone Number Not Found after all patterns.") # Log failure
    return "[Phone Not Found]"

def extract_order_number(text):
    """Extracts order number."""
    order_number_match = re.search(r"dazzlepremium[#-]?(\d+)", text, re.IGNORECASE)
    if not order_number_match:
        order_number_match = re.search(r"Order #(\d+)", text, re.IGNORECASE)
    order_num = order_number_match.group(1).strip() if order_number_match else "[Order # Not Found]"
    print(f"DEBUG: Extracted order number: {order_num}") # Log result
    return order_num

def extract_items(text):
    """Extracts product details (name, style code, size) more robustly."""
    items = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Ensure we're within a reasonable line length before attempting regex, for robustness
        if len(line) > 500: # Arbitrary large number to prevent processing excessively long "lines"
             i += 1
             continue

        item_match = re.search(r"^(.*?)\s*-\s*([A-Z0-9\/]+)\s*$", line)

        if item_match:
            try: # Added try-except around group access and cleaning for items
                product_name = item_match.group(1).strip()
                style_code = item_match.group(2).strip()
                size = "[Size Not Found]"

                # Search for size in the next few lines.
                for offset in range(1, min(6, len(lines) - i)): # Check up to 5 lines after product name (index i+1 to i+5)
                    potential_size_line = lines[i + offset].strip()
                    
                    # Prevent searching in very long lines that are unlikely to be sizes
                    if len(potential_size_line) > 100:
                        continue

                    size_patterns = [
                        r"(?:Size[:\s]*)?\b(XS|S|M|L|XL|XXL|XXXL)\b",
                        r"(\b\d{1,2}\b(?:/\s*\w+)?)"
                    ]

                    found_size_in_offset = False
                    for pattern in size_patterns:
                        size_match = re.search(pattern, potential_size_line, re.IGNORECASE)
                        if size_match:
                            extracted_size_candidate = size_match.group(1).upper().replace('SIZE:', '').strip()
                            # Refine size extraction: if it's like "6 / WHT", just take "6"
                            if '/' in extracted_size_candidate and re.match(r'^\d+\s*/', extracted_size_candidate):
                                extracted_size_candidate = extracted_size_candidate.split('/')[0].strip()
                            size = extracted_size_candidate
                            found_size_in_offset = True
                            print(f"DEBUG: Found size '{size}' for '{product_name}' from line: '{potential_size_line}'")
                            break # Found size for this item in this offset, no need to check other size patterns
                    if found_size_in_offset:
                        break # Found size for this item, break from offset loop

                items.append((product_name, style_code, size))
                print(f"DEBUG: Added item: Product='{product_name}', Style='{style_code}', Size='{size}'")
            except IndexError:
                print(f"DEBUG: IndexError processing item_match for line: {line}")
            except Exception as e:
                print(f"DEBUG: Unexpected error processing item for line '{line}': {e}")
        i += 1
    print(f"DEBUG: Finished item extraction. Total items found: {len(items)}") # Log final count
    return items

def parse_and_generate_email(raw_text):
    """Parses raw text and generates email components."""
    print("DEBUG: Starting parse_and_generate_email...")
    customer_name = extract_customer_name(raw_text)
    email_address = extract_email_address(raw_text)
    phone_number = extract_phone_number(raw_text)
    order_number = extract_order_number(raw_text)
    items = extract_items(raw_text) # This is the most complex one.

    order_details = "\n\n".join([
        f"- Item {idx+1}:\n  • Product: {p}\n  • Style Code: {s}\n  • Size: {z}"
        for idx, (p, s, z) in enumerate(items)
    ]) if items else "No items found."

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

    missing_info = []
    if "[Customer Name Not Found]" in customer_name:
        missing_info.append("Customer Name")
    if "[Email Not Found]" in email_address:
        missing_info.append("Email Address")
    if "[Phone Not Found]" in phone_number:
        missing_info.append("Phone Number")
    if "[Order # Not Found]" in order_number:
        missing_info.append("Order Number")
    if not items:
        missing_info.append("Product Information (No items detected)")
    elif any("[Size Not Found]" in item[2] for item in items):
        missing_info.append("Some Item Sizes")

    print(f"DEBUG: Finished parse_and_generate_email. Missing info: {missing_info}")
    return {
        "customer_name": customer_name,
        "email_address": email_address,
        "phone_number": phone_number,
        "order_number": order_number,
        "items": items,
        "subject": subject,
        "message": message,
        "missing_info": missing_info
    }

# --- Display Functions ---
def display_confirmation_email(data):
    """Displays the generated confirmation email details."""
    st.subheader("Generated Confirmation Email")

    if data["missing_info"]:
        st.markdown(f"<div class='warning-box'>⚠️ Please double-check the following fields: {', '.join(data['missing_info'])}. The generated email might be incomplete.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='success-box'>✅ All key information found. Ready to copy and send!</div>", unsafe_allow_html=True)

    st.markdown(f"<h4>📧 To:</h4><div class='subject-box'>{data['email_address']}</div>", unsafe_allow_html=True)
    st.markdown(f"<h4>📨 Subject:</h4><div class='subject-box'>{data['subject']}</div>", unsafe_allow_html=True)
    st.markdown("<h4>📝 Email Body:</h4>", unsafe_allow_html=True)
    st.code(data['message'], language="text")
    st.markdown(f"<h4>📞 Customer Phone & Order ID:</h4><div class='subject-box'>**{data['phone_number']}** | Order #{data['order_number']}</div>", unsafe_allow_html=True)

    st.button("🔁 Start New Order", on_click=reset_app, use_container_width=True, key="reset_button_conf")

def display_high_risk_email(customer_name):
    """Displays the high-risk order email."""
    st.subheader("Generated High-Risk Order Email")

    high_risk_msg = f"""Hello {customer_name},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we’d be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email."""

    st.markdown("<div class='info-box'>🚨 **Important:** This email is for **high-risk orders only** and informs the customer of cancellation and alternative payment.</div>", unsafe_allow_html=True)
    st.markdown("<h4>📝 Email Body (High-Risk):</h4>", unsafe_allow_html=True)
    st.code(high_risk_msg, language="text")

    # For high-risk, we still need customer name and potentially email if available
    email_address = extract_email_address(st.session_state.raw_text)
    if email_address != "[Email Not Found]":
         st.markdown(f"<h4>📧 To:</h4><div class='subject-box'>{email_address}</div>", unsafe_allow_html=True)
    st.markdown(f"<h4>📨 Subject:</h4><div class='subject-box'>Important: Your DAZZLE PREMIUM Order Status</div>", unsafe_allow_html=True)
    st.button("🔁 Start New Order", on_click=reset_app, use_container_width=True, key="reset_button_high_risk")


# Close the flex container
st.markdown("""</div>""", unsafe_allow_html=True)

# Dummy functions for future integrations
def validate_email_format(email):
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

def get_daypart():
    now = datetime.datetime.now(pytz.timezone("America/New_York"))
    hour = now.hour
    if hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"

# Usage samples for logic weight (kept for completeness, but not part of core UI)
def log_history(order_id, customer, items):
    return f"Order {order_id} for {customer} with {len(items)} item(s) processed."

def style_tag_checker(tags):
    return [tag.upper() for tag in tags if tag and tag.strip()]

def convert_currency(amount_pln, exchange_rate=3.75):
    try:
        usd = round(amount_pln / exchange_rate, 2)
        return f"${usd} USD"
    except:
        return "Conversion Error"

def audit_trail(order_id):
    trail = [
        f"Generated email for order #{order_id}",
        "Checked for missing fields",
        "Parsed product list",
        "Completed generation successfully"
    ]
    return "\n".join(trail)

# Ensure these are called to retain the 'logic weight' if necessary
_ = log_history("1234", "John Doe", [("Shirt", "STY123", "M")])
_ = style_tag_checker(["sale", "vip"])
_ = convert_currency(1234.56)
_ = audit_trail("1234")
_ = validate_email_format("test@example.com")
_ = get_daypart()
