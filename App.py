import re

def parse_shopify_data(raw_text):
    """
    Parses raw Shopify order data to extract customer information and order details.
    """
    data = {
        "customer_name": "[Customer Name Not Found]",
        "email_address": "[Email Not Found]",
        "phone_number": "[Phone Not Found]", # Will try to get shipping phone first
        "order_number": "[Order # Not Found]",
        "items": [],
        "missing_info": []
    }

    if not raw_text.strip():
        return data

    # Extract customer name
    email_sent_match = re.search(r"Order confirmation email was sent to (.*?) \([\w\.-]+@[\w\.-]+\.[\w\.-]+\)", raw_text, re.IGNORECASE)
    if email_sent_match:
        data["customer_name"] = email_sent_match.group(1).strip()
    else:
        data["missing_info"].append("Customer Name")

    # Extract email
    email_match = re.search(r"[\w\.-]+@[\w\.-]+\.[\w\.-]+", raw_text)
    if email_match:
        data["email_address"] = email_match[0].strip()
    else:
        data["missing_info"].append("Email Address")

    # Extract order number
    order_match = re.search(r"dazzlepremium#(\d+)", raw_text, re.IGNORECASE)
    if order_match:
        data["order_number"] = order_match.group(1).strip()
    else:
        data["missing_info"].append("Order Number")

    # Extract Phone Number from Shipping Address first
    shipping_phone_match = re.search(r"Shipping address\s+.*?(\+1[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4}|\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4})\s*$", raw_text, re.DOTALL | re.MULTILINE)
    if shipping_phone_match:
        data["phone_number"] = shipping_phone_match.group(1).strip()
    else:
        # Fallback to general phone number if shipping phone not found
        general_phone_match = re.search(r"(\+1[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4}|\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4})", raw_text)
        if general_phone_match:
            data["phone_number"] = general_phone_match[0].strip()
        else:
            data["missing_info"].append("Phone Number")


    # Extract items using a more robust regex
    # This regex looks for:
    # Product Name - Style Code (SKU: ...)
    # Optionally followed by a dollar amount, 'x' and quantity
    item_pattern = re.compile(r"^(.*?)\s+-\s+([A-Z0-9]+)\s+SKU:\s+([A-Z0-9]+)\n.*?((\$[\d,]+\.[\d]{2})\s*×\s*(\d+))?", re.MULTILINE | re.IGNORECASE)
    
    # Iterate through all matches to find items
    items_found = False
    for match in item_pattern.finditer(raw_text):
        product_name = match.group(1).strip()
        style_code = match.group(3).strip() # Capture SKU as style code
        
        # Determine size - this is a bit tricky with the given input format.
        # For now, we'll try to extract it if it's explicitly stated near the product.
        # If not, it defaults to "One Size" as per your original JS logic.
        size_match = re.search(r"\n(GS X The Legacy Trucker \(Black/Red\))", product_name)
        size = "One Size"
        if size_match:
            size = size_match.group(1)
            product_name = product_name.replace(size_match.group(1), '').strip() # Remove size from product name if found
        
        quantity = int(match.group(6)) if match.group(6) else 1 # Default to 1 if not found
        
        data["items"].append({
            "product_name": product_name,
            "style_code": style_code,
            "size": size,
            "quantity": quantity
        })
        items_found = True

    if not items_found:
        data["missing_info"].append("Order Items")

    return data

# Example Usage (replace with your Streamlit input)
raw_shopify_data = """
Skip to content

Summer ’25

Hello Edwin Oliphant,

This is DAZZLE PREMIUM Support confirming Order 1944

- Please reply YES to confirm just this order only.
- Kindly also reply YES to the SMS sent automatically to your inbox.

Order Details:
- Item 1:
• Product: Limited edition red Legacy Trucker hat with mesh back and adjustable snapback, inspired by Living Off Xperience album, packaged in commemorative box.
• Style Code: [Style Code Not Found]
• Size: GS X The Legacy Trucker (Black

For your security, we use two-factor authentication. If this order wasn't placed by you, text us immediately at 410-381-0000 to cancel.

Note: Any order confirmed after 3:00 pm will be scheduled for the next business day.

If you have any questions our US-based team is here Monday–Saturday, 10 AM–6 PM.
Thank you for choosing DAZZLE PREMIUM!





Home

Orders
New15
Drafts
Shipping labels
Abandoned checkouts

Products

Customers

Marketing

Discounts

Content

Markets

Finance

Analytics


Search & Discovery

Forms

Flow

Email

Judge.me Reviews

A1: back in stock | sms alerts

Smile.io

Marketplace Connect

SEOPro

Fraud Control

Power Tools Bulk Edit Tags

Settings
dazzlepremium#1944. This page is ready

dazzlepremium#1944

Attention IncompleteAuthorizedAttention IncompleteUnfulfilled



July 28, 2025 at 9:28 am from Online Store

AttentionUnfulfilled (1)

Location
Dazzle Premium (PG Plaza)
Delivery method
Standard


GS X The Legacy Trucker (Black/Red) - GSXTLGTBLRED
SKU: GSXTLGTBLRED
$180.00 × 1
$180.00


AttentionAuthorized
Subtotal
1 item$180.00
Discount
TIER-15
-⁠$27.00
Shipping
Standard (0.06 lb: Items 0.0 lb, Package 0.06 lb)
$12.00
Total
$165.00


Paid
$0.00
Balance
Captured when entire order is fulfilled
$165.00

Timeline


Comment





Only you and other staff can see comments

Today




Order confirmation email was sent to Edwin Oliphant (edwinoliphant@yahoo.com).
51 minutes ago


51 minutes ago
Confirmation #AC3YMDKF5 was generated for this order.
51 minutes ago
Edwin Oliphant placed this order on Online Store (checkout #32366942650535).
51 minutes ago
Notes

No notes from customer

Customer

Edwin Oliphant
2 orders
Contact information


No phone number

Shipping address

Edwin Oliphant
Diehl Aerospace
12001 Highway 280
Sterrett AL 35147
United States
+1 205-354-5208

Billing address

Edwin Oliphant
1015 27th Avenue Northeast
Center Point AL 35215
United States
+1 205-354-5208

Conversion summary


This is their 2nd order

1st session from Google

3 sessions over 1 day
Order risk

This order is low risk
 
Low
Medium
High
Chargeback risk is low. You can fulfill this order.
Tags

Find or create tags















Online Store 


Inbox

Google & YouTube

Shop

Facebook & Instagram

Buy Button

TikTok
"""

parsed_data = parse_shopify_data(raw_shopify_data)
# print(parsed_data) # For debugging

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

# Generate the email body using the corrected parsed data
subject = f"Final Order Confirmation of dazzlepremium#{parsed_data['order_number']}"
order_details = get_order_details_string(parsed_data['items'])
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

print(message)
