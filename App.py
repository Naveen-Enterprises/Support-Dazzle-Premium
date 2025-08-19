import streamlit as st
import re
import json
import html
import streamlit.components.v1 as components

# --- Page Configuration (new look) ---
st.set_page_config(page_title="DAZZLE PREMIUM — Email Studio", layout="wide", initial_sidebar_state="expanded")

# --- Initialize session state keys for new features ---
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = {}
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""
if "generated_subject" not in st.session_state:
    st.session_state.generated_subject = ""
if "generated_email_body" not in st.session_state:
    st.session_state.generated_email_body = ""
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "tone" not in st.session_state:
    st.session_state.tone = "Friendly"
if "saved_templates" not in st.session_state:
    st.session_state.saved_templates = []  # list of {"name":..., "subject":..., "body":..., "tone":...}
if "edited_parsed_json" not in st.session_state:
    st.session_state.edited_parsed_json = ""


# --- New CSS: totally different theme (gradient hero, cards, compact controls) ---
THEME_CSS = """
<style>
:root{
  --bg:#0f1724;
  --card:#0b1320;
  --muted:#9aa4b2;
  --accent:#ff7a59;
  --glass: rgba(255,255,255,0.03);
  --success:#2dd4bf;
}
body, .stApp {
  background: linear-gradient(180deg, #071025 0%, #071022 100%) fixed;
  color: #e6eef8;
  font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
}
.header {
  padding: 28px;
  border-radius: 12px;
  background: linear-gradient(90deg, rgba(255,122,89,0.12), rgba(45,212,191,0.06));
  display:flex; align-items:center; gap:18px; margin-bottom:18px;
}
.brand {
  width:64px; height:64px; border-radius: 12px;
  background: linear-gradient(135deg, #ff7a59, #2dd4bf);
  display:flex; justify-content:center; align-items:center; font-weight:700; color:#051025;
  box-shadow: 0 6px 18px rgba(0,0,0,0.5);
}
.hero-title { font-size:1.4rem; margin:0; font-weight:700; }
.hero-sub { color:var(--muted); margin:0; font-size:0.9rem; }

.card {
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.03);
  border-radius:10px; padding:14px;
}
.input-area textarea {
  width:100%; height:420px; resize:vertical; background:transparent; color:inherit; border:1px dashed rgba(255,255,255,0.04);
  padding:12px; border-radius:8px;
}
.controls .stButton>button { background:var(--accent); color:#051025; border:none; font-weight:700; }
.small-btn { background:transparent; border:1px solid rgba(255,255,255,0.04); color:var(--muted); padding:6px 8px; border-radius:6px; }
.preview-title { display:flex; justify-content:space-between; align-items:center; gap:12px; }
.preview-html { background: #051025; padding:12px; border-radius:8px; min-height:220px; overflow:auto; }
.field-input { background:transparent; color:inherit; border:1px solid rgba(255,255,255,0.03); padding:8px; border-radius:6px; width:100%; }
.tag { font-size:12px; color:var(--muted); }
.template-list { max-height:160px; overflow:auto; }
.footer-note { color:var(--muted); font-size:13px; margin-top:8px; }
.dark .card, .dark .preview-html { box-shadow: 0 8px 30px rgba(2,6,23,0.6); }
.light body, .light .stApp { background:#f6f8fb; color:#0b1320; }
.light .card { background:white; border:1px solid #eef2f7; color:#0b1320; }
.light .brand { color:white; }
.copy-button { background:#08263a; color:#bfefff; padding:8px 12px; border-radius:8px; border:none; }
@media(max-width:900px){
  .input-area textarea{ height:260px; }
}
</style>
"""

# JS for theme toggling and copy helper
THEME_JS = """
<script>
function applyTheme(isDark){
  const root = document.querySelector('.stApp');
  if(!root) return;
  if(isDark) root.classList.add('dark');
  else root.classList.remove('dark');
}
function copyToClipboard(text, btnId){
    navigator.clipboard.writeText(text).then(()=>{
        const el = document.getElementById(btnId);
        if(el){ const old = el.innerText; el.innerText='Copied'; setTimeout(()=>el.innerText=old,1200); }
    });
}
</script>
"""

# Inject theme CSS + JS
st.markdown(THEME_CSS + THEME_JS, unsafe_allow_html=True)

# Immediately apply theme using a small script
st.markdown(f"<script>applyTheme({str(st.session_state.dark_mode).lower()});</script>", unsafe_allow_html=True)


# ------------------------------
# Parser (kept robust, slightly trimmed for brevity)
# ------------------------------
def parse_shopify_export(raw_text_input):
    """
    Parses the raw Shopify order export text to extract key information.
    This function uses multiple, redundant regex patterns and fallback strategies
    to maximize extraction success without human intervention.
    """
    data = {
        "customer_name": "[Customer Name Not Found]",
        "email_address": "[Email Not Found]",
        "phone_number": "[Phone Not Found]",
        "order_number": "[Order # Not Found]",
        "items": [],
        "missing_info": []
    }

    # Reuse original parsing heuristics (condensed)
    normalized_text = raw_text_input or ""
    lines = [line.strip() for line in normalized_text.splitlines() if line.strip()]

    # Name
    m = re.search(r"Order confirmation email was sent to (.*?) \([\w\.-]+@[\w\.-]+\.[\w\.-]+\)", normalized_text, re.IGNORECASE)
    if m:
        data["customer_name"] = m.group(1).strip()
    else:
        for i, line in enumerate(lines):
            if re.search(r"^(Customer|Contact information)$", line, re.IGNORECASE):
                if i+1 < len(lines) and "@" not in lines[i+1]:
                    data["customer_name"] = lines[i+1]
                    break
    if data["customer_name"].startswith("["):
        data["missing_info"].append("Customer Name")

    # Email
    m = re.search(r"[\w\.-]+@[\w\.-]+\.[\w\.-]+", normalized_text)
    if m:
        data["email_address"] = m.group(0)
    else:
        data["missing_info"].append("Email Address")

    # Phone
    m = re.search(r"(\+1[\s\-()]?\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4}|\d{3}[\s\-()]?\d{3}[\s\-()]?\d{4})", normalized_text)
    if m:
        data["phone_number"] = m.group(0)
    else:
        data["missing_info"].append("Phone Number")

    # Order number
    m = re.search(r"dazzlepremium#?(\d+)", normalized_text, re.IGNORECASE) or re.search(r"(?:Order #|Order Number|Invoice #)\s*(\d+)", normalized_text, re.IGNORECASE)
    if m:
        data["order_number"] = m.group(1)
    else:
        data["missing_info"].append("Order Number")

    # Items: simple heuristic capturing lines with price or dash-coded items
    items = []
    for i, line in enumerate(lines):
        if re.search(r"\$\d+\.\d{2}", line) and not any(k in line.lower() for k in ["subtotal","shipping","tax","total"]):
            name = lines[i-1] if i>0 else line
            name = re.sub(r"\s*\$\d+\.\d{2}.*","",name).strip()
            # try to get size/qty from next lines
            size = "Size Not Found"; qty = 1; style = "N/A"
            if i+1 < len(lines) and re.search(r"x\s*\d+", lines[i+1], re.IGNORECASE):
                q = re.search(r"x\s*(\d+)", lines[i+1], re.IGNORECASE)
                if q: qty = int(q.group(1))
            items.append({"product_name": name, "style_code": style, "size": size, "quantity": qty})
    # fallback: look for lines containing " - " pattern
    if not items:
        for line in lines:
            if " - " in line and not any(k in line.lower() for k in ["subtotal","shipping","tax","total"]):
                parts = line.rsplit(" - ",1)
                items.append({"product_name": parts[0].strip(), "style_code": parts[1].strip(), "size":"Size Not Found", "quantity":1})

    data["items"] = items
    if not items:
        data["missing_info"].append("Order Items")
    # detect sizes missing
    if any(it.get("size","") == "Size Not Found" for it in items):
        data.setdefault("missing_info",[]).append("Item Sizes")
    return data


# ------------------------------
# Generators (now accept tone and edited parsed data)
# ------------------------------
def generate_email(parsed_data, tone="Friendly", mode="standard"):
    # Basic building blocks influenced by tone
    name = parsed_data.get("customer_name","Customer")
    order_num = parsed_data.get("order_number","[Order # Not Found]")
    items = parsed_data.get("items", [])
    phone = parsed_data.get("phone_number", "410-381-0000")

    # Tone adjustments
    greetings = {
        "Friendly": f"Hi {name},",
        "Formal": f"Hello {name},",
        "Urgent": f"Attention {name},"
    }
    closings = {
        "Friendly": "Thanks for choosing DAZZLE PREMIUM! — The Support Team",
        "Formal": "Sincerely,\nDAZZLE PREMIUM Support",
        "Urgent": "Please respond immediately to avoid cancellation.\nDAZZLE PREMIUM Support"
    }
    # Compose order details compactly
    details = []
    for idx, it in enumerate(items, start=1):
        qty_str = f" (x{it.get('quantity',1)})" if it.get('quantity',1)>1 else ""
        details.append(f"{idx}. {it.get('product_name','N/A')} — {it.get('style_code','N/A')} — {it.get('size','Size Not Found')}{qty_str}")
    details_text = "\n".join(details) if details else "No items found."

    if mode == "standard":
        subject = f"Final Order Confirmation — dazzlepremium#{order_num}"
        body = f"""{greetings[tone]}

This is DAZZLE PREMIUM Support confirming Order #{order_num}.

Order Summary:
{details_text}

Please reply YES to this email to confirm this order. You may also confirm via the SMS sent to your phone.

For your security, if this order wasn’t placed by you, text us immediately at {phone}.

{closings[tone]}"""
    elif mode == "high_risk":
        subject = f"Important: Order {order_num} Flagged — Action Required"
        body = f"""{greetings[tone]}

Your order {order_num} was flagged and auto-cancelled for security reasons. If you'd like to proceed, reply and follow the secure payment instructions.

{closings[tone]}"""
    elif mode == "return":
        subject = f"Return Instructions for Order #{order_num}"
        body = f"""Dear {name},

Please ship returns to:
Dazzle Premium
3500 East-West Highway
Suite 1032
Hyattsville, MD 20782

Once shipped, reply with the tracking number and we'll process your refund.

{closings[tone]}"""
    elif mode == "medium_risk":
        subject = f"Verification Needed — dazzlepremium#{order_num}"
        body = f"""{greetings[tone]}

Your order #{order_num} requires manual verification before shipping.

Order Details:
{details_text}

Please reply with:
- Order number
- Photo ID (name visible)
- Photo of payment card (cover digits except last 4)

We will review promptly.

{closings[tone]}"""
    else:
        subject = f"Message regarding order #{order_num}"
        body = f"{greetings[tone]}\n\n{details_text}\n\n{closings[tone]}"

    return subject, body


# ------------------------------
# Helper: pretty HTML from plain text (basic conversion)
# ------------------------------
def plain_to_html(text):
    escaped = html.escape(text)
    # simple transforms: blank line -> <p>, bullets -> <li>
    parts = [p.strip() for p in escaped.split("\n\n")]
    html_parts = []
    for p in parts:
        lines = p.splitlines()
        if all(re.match(r"^\d+\. ", line) for line in lines):
            # numbered
            lis = "".join(f"<li>{ln.split('. ',1)[1]}</li>" for ln in lines)
            html_parts.append(f"<ol style='margin:6px 0 12px 16px'>{lis}</ol>")
        elif all(re.match(r"^•|^- ", line) for line in lines):
            lis = "".join(f"<li>{ln.lstrip('•- ').strip()}</li>" for ln in lines)
            html_parts.append(f"<ul style='margin:6px 0 12px 16px'>{lis}</ul>")
        else:
            p_html = "<br>".join(lines)
            html_parts.append(f"<p style='margin:6px 0 10px'>{p_html}</p>")
    wrapper = "<div style='font-family:Inter,Arial; color:#e6eef8; line-height:1.4;'>" + "".join(html_parts) + "</div>"
    return wrapper


# ------------------------------
# Reset routine (keeps new keys)
# ------------------------------
def reset_app_state():
    st.session_state.raw_text = ""
    st.session_state.parsed_data = {}
    st.session_state.generated_subject = ""
    st.session_state.generated_email_body = ""
    st.session_state.edited_parsed_json = ""
    st.experimental_rerun()


# ------------------------------
# UI Layout (completely new)
# ------------------------------
# Header
st.markdown("""
<div class="header card">
  <div class="brand">DP</div>
  <div>
    <div class="hero-title">DAZZLE PREMIUM — Email Studio</div>
    <div class="hero-sub">Revamped generator • tone controls • templates • live HTML preview • downloads</div>
  </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3,2,3])

# Left: Input & Bulk support
with col1:
    st.markdown("<div class='card input-area'>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px'><strong>Paste Shopify Export</strong><span class='tag'>Supports single export</span></div>", unsafe_allow_html=True)
    raw = st.text_area("", value=st.session_state.raw_text, key="raw_text_area", placeholder="Paste raw Shopify order export here (or multiple separated with --- for quick demos)...")
    st.markdown("</div>", unsafe_allow_html=True)

    # Quick actions under input
    st.markdown("<div style='display:flex; gap:8px; margin-top:10px'>", unsafe_allow_html=True)
    if st.button("Parse & Preview", key="parse_btn"):
        st.session_state.raw_text = raw
        parsed = parse_shopify_export(raw)
        st.session_state.parsed_data = parsed
        # populate editable json for items
        st.session_state.edited_parsed_json = json.dumps(parsed, indent=2)
        st.session_state.generated_subject, st.session_state.generated_email_body = generate_email(parsed, tone=st.session_state.tone, mode="standard")
        # removed experimental_rerun() - Streamlit will rerun automatically after button press
    st.markdown("<button class='small-btn' id='clearBtn'>Clear</button>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    # Clear button JS hook
    st.markdown("""
    <script>
    const cbtn = document.getElementById('clearBtn');
    if(cbtn){ cbtn.onclick = ()=>{ const ta = document.querySelector('textarea'); if(ta){ ta.value=''; ta.dispatchEvent(new Event('input')); } } }
    </script>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<strong>Bulk demo tip</strong><div class='tag'>You can paste multiple order exports separated by lines '---' and copy each parsed result manually for quick demos.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# Middle: Controls & Editable parsed data + tone and templates
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<strong>Controls</strong>", unsafe_allow_html=True)
    # Theme toggle
    dark = st.checkbox("Dark Mode", value=st.session_state.dark_mode, key="dark_toggle")
    if dark != st.session_state.dark_mode:
        st.session_state.dark_mode = dark
        st.markdown(f"<script>applyTheme({str(dark).lower()});</script>", unsafe_allow_html=True)

    tone = st.radio("Tone", options=["Friendly","Formal","Urgent"], index=["Friendly","Formal","Urgent"].index(st.session_state.tone), key="tone_radio")
    st.session_state.tone = tone

    st.markdown("<div style='margin-top:10px'><strong>Saved Templates</strong></div>", unsafe_allow_html=True)
    # Save / load templates
    name_for_save = st.text_input("Template name", key="template_name")
    col_save, col_load = st.columns([1,1])
    with col_save:
        if st.button("Save Template", key="save_template_btn"):
            tpl = {"name": name_for_save or f"Template {len(st.session_state.saved_templates)+1}",
                   "subject": st.session_state.generated_subject,
                   "body": st.session_state.generated_email_body,
                   "tone": st.session_state.tone}
            st.session_state.saved_templates.insert(0, tpl)
            st.success("Template saved")
    with col_load:
        choices = [t.get("name") for t in st.session_state.saved_templates]
        if choices:
            sel = st.selectbox("Load template", options=["(select)"]+choices, key="load_select")
            if sel and sel != "(select)":
                tpl = next((t for t in st.session_state.saved_templates if t["name"]==sel), None)
                if tpl:
                    st.session_state.generated_subject = tpl["subject"]
                    st.session_state.generated_email_body = tpl["body"]
                    st.session_state.tone = tpl.get("tone","Friendly")
                    # removed experimental_rerun() - UI will update on state change

        else:
            st.markdown("<div class='tag'>No saved templates yet.</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<strong>Edit parsed data (JSON)</strong>", unsafe_allow_html=True)
    edited_json = st.text_area("", value=st.session_state.edited_parsed_json, height=220, key="edited_json_area")
    if st.button("Apply Edits", key="apply_edits_btn"):
        try:
            parsed = json.loads(edited_json)
            # basic validation
            if not isinstance(parsed, dict):
                st.error("JSON must be an object/dictionary.")
            else:
                st.session_state.parsed_data = parsed
                st.session_state.edited_parsed_json = json.dumps(parsed, indent=2)
                st.success("Applied edits")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


# Right: Preview, copy, download, export
with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='preview-title'><strong>Live Preview</strong><div><span class='tag'>Tone:</span>&nbsp;<strong>"+st.session_state.tone+"</strong></div></div>", unsafe_allow_html=True)

    # Buttons row
    bcol1, bcol2, bcol3 = st.columns([1,1,1])
    with bcol1:
        if st.button("Generate Standard", key="gen_std"):
            subj, body = generate_email(st.session_state.parsed_data or {}, tone=st.session_state.tone, mode="standard")
            st.session_state.generated_subject, st.session_state.generated_email_body = subj, body
            # removed experimental_rerun()

    with bcol2:
        if st.button("Generate Medium-Risk", key="gen_med"):
            subj, body = generate_email(st.session_state.parsed_data or {}, tone=st.session_state.tone, mode="medium_risk")
            st.session_state.generated_subject, st.session_state.generated_email_body = subj, body
            # removed experimental_rerun()

    with bcol3:
        if st.button("Generate High-Risk", key="gen_high"):
            subj, body = generate_email(st.session_state.parsed_data or {}, tone=st.session_state.tone, mode="high_risk")
            st.session_state.generated_subject, st.session_state.generated_email_body = subj, body
            # removed experimental_rerun()

    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
    # Recipient / subject display
    recipient = st.session_state.parsed_data.get("email_address","[Email Not Found]")
    recipient_js = json.dumps(recipient)
    st.markdown(
        f"<div style='display:flex; gap:8px; align-items:center;'>"
        f"<div style='flex:1'><div class='tag'>To</div><div style='font-weight:700'>{recipient}</div></div>"
        f"<div><button class='copy-button' id='copyToBtn' onclick=\"copyToClipboard({recipient_js}, 'copyToBtn')\">Copy</button></div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    subject_js = json.dumps(st.session_state.generated_subject)
    st.markdown(
        f"<div style='margin-top:8px; display:flex; gap:8px; align-items:center;'>"
        f"<div style='flex:1'><div class='tag'>Subject</div><div style='font-weight:700'>{st.session_state.generated_subject}</div></div>"
        f"<div><button class='copy-button' id='copySubBtn' onclick=\"copyToClipboard({subject_js}, 'copySubBtn')\">Copy</button></div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Tabs: Plain, HTML Preview, Export
    tabs = st.tabs(["Plain", "HTML Preview", "Export"])
    with tabs[0]:
        st.text_area("Email Body (plain)", value=st.session_state.generated_email_body, height=260, key="plain_body")
        st.markdown("<div style='display:flex; gap:8px; margin-top:8px'>", unsafe_allow_html=True)
        if st.button("Copy Body", key="copy_body_btn"):
            # use JS clipboard via injected script
            st.markdown(f"<script>copyToClipboard({json.dumps(st.session_state.generated_email_body)}, 'copy_body_btn');</script>", unsafe_allow_html=True)
        # Download as .txt and .eml
        export_txt = f"Subject: {st.session_state.generated_subject}\n\n{st.session_state.generated_email_body}"
        st.download_button("Download .txt", data=export_txt, file_name=f"order_{st.session_state.parsed_data.get('order_number','0')}.txt", mime="text/plain")
        eml = f"Subject: {st.session_state.generated_subject}\nTo: {recipient}\n\n{st.session_state.generated_email_body}"
        st.download_button("Download .eml", data=eml, file_name=f"order_{st.session_state.parsed_data.get('order_number','0')}.eml", mime="message/rfc822")
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        html_preview = plain_to_html(st.session_state.generated_email_body or "No content generated yet.")
        components.html(html_preview, height=320, scrolling=True)

    with tabs[2]:
        st.markdown("<div style='display:flex; gap:8px; align-items:center'>", unsafe_allow_html=True)
        if st.button("Save as Template", key="export_save_tpl"):
            tpl = {"name": name_for_save or f"Template {len(st.session_state.saved_templates)+1}",
                   "subject": st.session_state.generated_subject,
                   "body": st.session_state.generated_email_body,
                   "tone": st.session_state.tone}
            st.session_state.saved_templates.insert(0,tpl)
            st.success("Saved to templates")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='footer-note'>Tip: Use downloads to attach to your email client or save templates for repeated responses.</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# Bottom utility row
st.markdown("<div style='display:flex; gap:12px; margin-top:12px'>", unsafe_allow_html=True)
if st.button("Reset All", key="reset_all"):
    reset_app_state()
st.markdown("<div style='margin-left:auto; color:var(--muted)'>DAZZLE PREMIUM — Email Studio • Demo mode</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
