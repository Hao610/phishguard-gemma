"""
PhishGuard - Built for a Friend
A Privacy-First Open Source AI Email & SMS Phishing Forensic Shield
Powered by Gemma 2 Open Weights
"""

import streamlit as st
import json
import time
from engine import PhishGuardEngine

st.set_page_config(
    page_title="PhishGuard | Built for Alex",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Cyber-Defense UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00e5ff;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #94a3b8;
        margin-bottom: 25px;
    }
    .metric-card {
        background: #0f172a;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #1e293b;
    }
    .stButton>button {
        background: linear-gradient(90deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: Context & Story
with st.sidebar:
    st.markdown("## 🛡️ **PhishGuard**")
    st.markdown("`Powered by Google Gemma 2`")
    st.info(
        "**Built for my friend Alex:**\n\n"
        "Alex recently received a targeted fake university bursary email with his real student ID and nearly entered his banking details.\n\n"
        "He hesitated to paste the email into ChatGPT because it contained personal PII (Full name, student ID, bank reference). "
        "**PhishGuard was built to solve this: 100% private, local-first open AI auditing with Gemma 2.**"
    )

    st.markdown("---")
    st.markdown("### ⚙️ Engine Settings")
    model_choice = st.selectbox(
        "Inference Backbone",
        ["Gemma 2 (2B / 9B Open Weights)", "Local Air-Gapped Heuristics"],
        index=0
    )
    api_key = st.text_input("Optional Gemma/Gemini API Key (for cloud demo)", type="password")

    st.markdown("---")
    st.caption("🏆 Hacktoberfest 2026: Build for a Friend | Best Use of Gemma & Render")

# Main Interface
st.markdown('<div class="main-header">🛡️ PhishGuard: Zero-Leakage Threat Scanner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Give your non-technical friends peace of mind without uploading their sensitive emails to big tech servers.</div>', unsafe_allow_html=True)

# Session state initialization for sample texts
sample_bank = """URGENT: Your Wells Fargo online access has been temporarily locked due to 3 suspicious login attempts from IP 192.168.1.1.
To prevent immediate account termination and legal escalations, you must verify your identity within 12 hours.
Click here to restore access: http://wellsfarg0.secure-banking-auth.com/verify?account=98231
Account Security Department"""

sample_bursary = """Dear Student (ID: 2024-88491),
Your student emergency bursary grant of $1,250.00 has been approved by the Student Financial Aid Committee.
Please confirm your disbursement direct deposit bank details within 24 hours to receive immediate wire transfer:
http://portal-bursary-edu.xyz/login
Office of the Registrar"""

sample_safe = """Hi Alex,
Just following up on our project discussion from yesterday. I uploaded the slides to our shared Google Drive folder.
Let me know when you have time for a quick 10-minute sync before Friday's lab.
Best,
Sarah"""

if "current_text" not in st.session_state:
    st.session_state.current_text = sample_bank

# Quick Sample Buttons
st.markdown("##### ⚡ Click to load a real-world scenario:")
col_s1, col_s2, col_s3 = st.columns(3)

if col_s1.button("🚨 Fake Bank Lockout (Urgency)", use_container_width=True):
    st.session_state.current_text = sample_bank
    st.rerun()

if col_s2.button("🎓 Fake Student Bursary (Spoofing)", use_container_width=True):
    st.session_state.current_text = sample_bursary
    st.rerun()

if col_s3.button("✅ Genuine Work Follow-up (Safe)", use_container_width=True):
    st.session_state.current_text = sample_safe
    st.rerun()

# Text Input
message_text = st.text_area(
    "Suspicious Email, SMS, or WhatsApp message to audit:",
    value=st.session_state.current_text,
    height=170,
    placeholder="Paste the raw text or email content here..."
)

analyze_btn = st.button("🔍 Audit This Message with Gemma", use_container_width=True)

if analyze_btn and message_text.strip():
    with st.spinner("Analyzing linguistic hooks, psychological urgency, and domain mimicry with Gemma..."):
        engine = PhishGuardEngine()
        time.sleep(0.5)  # smooth UI feel
        result = engine.analyze(message_text, api_key=api_key)

    st.markdown("---")
    
    # Verdict Cards
    c1, c2, c3 = st.columns([1.2, 1.8, 1.5])

    verdict = result.get("verdict", "SAFE")
    score = result.get("threat_score", 0)

    with c1:
        if verdict == "CRITICAL_PHISHING":
            st.error(f"### 🛑 DANGER: {verdict}")
            st.progress(score / 100.0)
            st.markdown(f"**Threat Index:** `{score}/100`")
        elif verdict == "SUSPICIOUS":
            st.warning(f"### ⚠️ CAUTION: {verdict}")
            st.progress(score / 100.0)
            st.markdown(f"**Threat Index:** `{score}/100`")
        else:
            st.success(f"### ✅ CLEAR: {verdict}")
            st.progress(score / 100.0)
            st.markdown(f"**Threat Index:** `{score}/100`")

    with c2:
        st.markdown("#### 📝 Plain-English Verdict for Your Friend")
        st.write(result.get("summary", ""))

    with c3:
        st.markdown("#### 🎯 Detected Deception Tactics")
        for tactic in result.get("detected_tactics", []):
            st.badge = st.markdown(f"- 🔴 **{tactic}**")

    # Actionable Advice
    st.markdown("### 🛡️ Recommended Action Plan for Alex")
    for idx, step in enumerate(result.get("safe_action_plan", []), 1):
        st.info(f"**Step {idx}:** {step}")

elif analyze_btn and not message_text.strip():
    st.warning("Please paste an email or choose a sample above first!")
