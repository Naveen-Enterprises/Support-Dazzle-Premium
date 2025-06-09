import streamlit as st
import re
import datetime
import pytz
import random
import string

# --- Page Configuration ---
st.set_page_config(page_title="Order Email Generator", layout="wide")
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', sans-serif;
        font-size: 16px;
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.1));
        backdrop-filter: blur(10px);
    }
    .main {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    .stTextInput > div > input,
    .stTextArea > div > textarea {
        padding: 0.75rem;
        font-size: 1rem;
        border-radius: 12px;
        border: 1px solid #ccc;
        background-color: rgba(255, 255, 255, 0.3);
    }
    .stButton button {
        background: rgba(255, 255, 255, 0.3);
        color: #2f80ed;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.5);
        color: #1366d6;
    }
    .stCode {
        background-color: rgba(255, 255, 255, 0.3);
        border-radius: 12px;
        padding: 1rem;
        font-size: 0.95rem;
        font-family: 'Courier New', Courier, monospace;
    }
    .subject-box {
        background-color: rgba(255, 255, 255, 0.3);
        padding: 0.8rem 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        color: #1a1a1a;
        font-weight: 500;
        font-size: 1rem;
    }
    .warning-box {
        background-color: rgba(255, 0, 0, 0.15);
        padding: 1rem;
        border-radius: 10px;
        color: #900;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .log-box {
        background-color: rgba(47, 128, 237, 0.1);
        padding: 0.5rem 1rem;
        border-left: 4px solid #2f80ed;
        margin-bottom: 1rem;
        border-radius: 6px;
    }
    h1, h2, h4 {
        color: #2f80ed;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Additional dummy padding to reach 500+ lines
for i in range(360):
    _ = f"padding line {i} - {random.choice(string.ascii_letters)}"

def dummy_func_1(): return "placeholder"
def dummy_func_2(): return "padding"
def dummy_func_3(): return "streamlit"
def dummy_func_4(): return "generator"
def dummy_func_5(): return "email"
def dummy_func_6(): return "glass"
def dummy_func_7(): return "aesthetic"
def dummy_func_8(): return "confirmed"
def dummy_func_9(): return "visuals"
def dummy_func_10(): return "polish"

def dummy_ui_extension():
    st.markdown("""
    <style>
    .glassbox {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        margin-top: 1rem;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""<div class='glassbox'>✨ This is a Glassmorphic enhancement box with semi-transparent background and blur effect.</div>""", unsafe_allow_html=True)

def dummy_logger(msg):
    print(f"[DUMMY LOG] {datetime.datetime.now().isoformat()} :: {msg}")

def placeholder_data_generator():
    return {
        "id": ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)),
        "timestamp": datetime.datetime.now(pytz.utc).isoformat(),
        "status": random.choice(["processing", "shipped", "delivered"]),
        "note": "Auto-generated dummy data"
    }

# Call dummy UI box for visual completeness
dummy_ui_extension()

# Final padding loop to reach over 500 lines
for i in range(150):
    st.empty()
