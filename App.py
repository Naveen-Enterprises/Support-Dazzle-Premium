import streamlit as st
import re

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="wide")

# --- Custom CSS for Apple-like Aesthetics ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    body { 
        font-family: 'Inter', sans-serif; 
        font-size: 16px; 
        color: #333333; /* Darker grey for body text */
        background-color: #F0F2F5; /* Light background */
    }
    .main { 
        background-color: #ffffff; /* Pure white for the main content area */
        padding: 3rem; /* More breathing room */
        border-radius: 16px; /* More rounded corners */
        box-shadow: 0 8px 30px rgba(0,0,0,0.08); /* Softer, more pronounced shadow */
        max-width: 1200px; /* Max width for better readability on large screens */
        margin: 2rem auto; /* Center the main content */
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        padding: 1rem;
        font-size: 1rem;
        border-radius: 10px;
        border: 1px solid #E0E0E0; /* Softer border */
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05); /* Subtle inner shadow */
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #007AFF; /* Apple Blue on focus */
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.08), 0 0 0 3px rgba(0,122,255,0.2); /* Glow effect */
        outline: none;
    }
    .stButton button {
        background-color: #007AFF; /* Apple Blue */
        color: white;
        font-weight: 600;
        padding: 0.9rem 1.8rem; /* Larger buttons */
        font-size: 1.05rem;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        transition: background-color 0.2s ease, transform 0.1s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 15px rgba(0,122,255,0.25); /* More prominent shadow */
    }
    .stButton button:hover {
        background-color: #005BB5; /* Darker blue on hover */
        transform: translateY(-2px); /* Lift effect */
        box-shadow: 0 6px 20px rgba(0,122,255,0.35);
    }
    .stButton button:active {
        transform: translateY(0);
        box-shadow: inset 0 1px 5px rgba(0,0,0,0.2); /* Pressed effect */
    }
    .stCode {
        background-color: #F7F8FA; /* Light gray for code blocks */
        border-radius: 10px;
        padding: 1.2rem;
        font-size: 0.95rem;
        border: 1px solid #E0E0E0;
        box-shadow: 0 1px 5px rgba(0,0,0,0.05);
    }
    .subject-box {
        background-color: #E6F2FF; /* Very light blue for info boxes */
        padding: 1rem 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        color: #005BB5; /* Darker blue text */
        font-weight: 500;
        font-size: 1.05rem;
        border: 1px solid #D0E8FF; /* Subtle border */
    }
    .warning-box {
        background-color: #FFF0F0; /* Light red for warnings */
        padding: 1.2rem;
        border-radius: 10px;
        color: #CC0000; /* Dark red text */
        font-weight: 600;
        margin-bottom: 1.5rem;
        border: 1px solid #FFCCCC;
    }
    .success-box {
        background-color: #E6FFE6; /* Light green for success */
        padding: 1.2rem;
        border-radius: 10px;
        color: #008000; /* Dark green text */
        font-weight: 600;
        margin-bottom: 1.5rem;
        border: 1px solid #CCFFCC;
    }
    h1, h2, h4 { 
        color: #1A1A1A; /* Dark charcoal for headings */
        font-weight: 700; 
        margin-bottom: 1rem; 
    } 
    h1 { 
        font-size: 2.8rem; /* Larger main title */
        text-align: center; 
        margin-bottom: 2.5rem; 
        letter-spacing: -0.02em; /* Tighter letter spacing */
    }
    h2 { font-size: 2rem; margin-bottom: 1.5rem; } /* Larger subheadings */
    h4 { font-size: 1.3rem; margin-bottom: 0.8rem; }
    .stAlert {
        border-radius: 10px;
        padding: 1rem;
    }
    .stAlert > div {
        border-radius: 10px !important;
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
    textarea.focus();
    textarea.select();
    try {
        document.execCommand('copy');
    } catch (err) {
        console.error('Copy command failed:', err);
    } finally {
        document.body.removeChild(textarea);
    }
}
</script>
"""
st.markdown(js_copy_function, unsafe_allow_html=True)

st.markdown("""<h1 style='text-align: center;'>📦 DAZZLE PREMIUM Order Email Generator</h1>""", unsafe_allow_html=True)

if "reset_clicked" not in st.session_state:
    st.session_state.reset_clicked = False

# Reset logic for "Start New Order" button
if st.session_state.reset_clicked:
    for key in ["raw_text_input", "display_email_body", "generated_email_body", "high_risk_email_body"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.reset_clicked = False
    st.rerun()

st.markdown("""<div style='display: flex; gap: 40px;'>""", unsafe_allow_html=True)

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Paste Shopify Order Export Here")
        # The core "no friction" input: email generates as text is typed/pasted
        raw_text = st.text_area("Order Details", height=500, key="raw_text_input", 
                                value=st.session_state.get("raw_text_input", ""), # Use the correct key for value
                                help="Paste the full Shopify order export text.")
        
        # High-Risk button remains a distinct action
        high_risk_action = st.button("🚨 Generate High-Risk Email")

    with col2:
        # Initialize message variables
        email_address = "[Email Not Found]"
        subject = "[Subject Not Generated]"
        message = ""
        phone_number = "[Phone Not Found]"
        customer_name = "[Customer Name Not Found]"
        missing_info = []

        # Logic for processing text and generating email
        if raw_text:
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

            # Construct Order Details string (Plain Text)
            order_details_list = []
            for idx, (p, s, z) in enumerate(items):
                item_prefix = ""
                if len(items) > 1:
                    item_prefix = f"- Item {idx+1}:\n"
                
                item_detail = f"{item_prefix}• Product: {p}\n• Size: {z}"
                
                if len(items) > 1:
                    item_detail += f"\n• Style Code: {s}"
                order_details_list.append(item_detail)

            order_details = "\n\n".join(order_details_list)

            # Construct Email Subject and Message (Plain Text)
            subject = f"Final Order Confirmation of dazzlepremium#{order_number}"
            
            message_lines = [
                f"Hello {customer_name},",
                "", 
                f"This is DAZZLE PREMIUM Support confirming Order {order_number}",
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
            message = "\n".join(message_lines)

            # Check for missing information and display warnings
            if "[Customer Name Not Found]" in customer_name: missing_info.append("Customer Name")
            if "[Email Not Found]" in email_address: missing_info.append("Email Address")
            if "[Phone Not Found]" in phone_number: missing_info.append("Phone Number")
            if "[Order # Not Found]" in order_number: missing_info.append("Order Number")
            if any("[Size Not Found]" in item[2] for item in items): missing_info.append("Item Sizes")

            # Store generated message in session state for copy button
            st.session_state.generated_email_body = message

        # High-risk email logic
        if high_risk_action:
            if not raw_text:
                st.warning("Please paste the order export before generating the high-risk message.")
            else:
                high_risk_msg = f"""Hello {customer_name},

We hope this message finds you well.

We regret to inform you that your recent order has been automatically cancelled as it was flagged as a high-risk transaction by our system. This is a standard security measure to help prevent unauthorized or fraudulent activity.

If you would still like to proceed with your order, we’d be happy to assist you in placing it manually. To do so, we kindly ask that you transfer the payment via Cash App.

Once the payment is received, we will immediately process your order and provide confirmation along with tracking details.

If you have any questions or need assistance, feel free to reply to this email."""
                st.session_state.generated_email_body = high_risk_msg
                # Overwrite message for display
                message = high_risk_msg
                missing_info = [] # Clear warnings for high-risk message

        # Display output only if raw_text is present or high_risk_action was clicked with raw_text
        if raw_text or (high_risk_action and raw_text):
            if missing_info:
                st.markdown(f"<div class='warning-box'>⚠️ Please double-check the following fields: {', '.join(missing_info)}</div>", unsafe_allow_html=True)
            elif raw_text and not high_risk_action: # Only show success for regular generation
                st.markdown("<div class='success-box'>✅ Email ready to copy.</div>", unsafe_allow_html=True)
            elif high_risk_action and raw_text: # Specific message for high-risk
                 st.markdown("<div class='warning-box'>⚠️ High-Risk Email Generated.</div>", unsafe_allow_html=True)


            st.markdown(f"<h4>📧 Email Address:</h4><div class='subject-box'>{email_address}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4>📨 Subject:</h4><div class='subject-box'>{subject}</div>", unsafe_allow_html=True)
            
            st.markdown("<h4>📋 Email Body:</h4>", unsafe_allow_html=True)
            # This is the single source of truth for the email body
            st.text_area("Email Body", value=st.session_state.get("generated_email_body", ""), height=350, key="display_email_body")
            
            # Copy button: directly calls the JS function
            # The key ensures the button is re-rendered correctly if the text area changes
            if st.button("✨ Copy Email to Clipboard", key="copy_button"):
                # Call the JS function defined globally
                st.components.v1.html(
                    f"<script>copyTextToClipboard(document.getElementById('display_email_body').value);</script>",
                    height=0, width=0
                )
                st.success("Copied to clipboard!") # Instant feedback

            st.markdown(f"<h4>📱 Phone Number:</h4><div class='subject-box'>{phone_number}</div>", unsafe_allow_html=True)
            
            # "Start New Order" button for resetting
            st.button("🔁 Start New Order", on_click=lambda: st.session_state.update({"reset_clicked": True}))

        elif not raw_text:
            st.info("Paste your Shopify order export on the left to begin.")


st.markdown("""</div>""", unsafe_allow_html=True)
