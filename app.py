"""
PhishGuard - Built for a Friend (Alex)
Privacy-Preserving Open Source Threat Forensics powered by Google Gemma 2
"""

import streamlit as st
import json
import time
from engine import PhishGuardEngine

st.set_page_config(
    page_title="PhishGuard | Shield for Alex",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Tech Cyber UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    .report-box {
        background-color: #0b1120;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 15px;
        font-family: monospace;
        font-size: 0.85rem;
        color: #38bdf8;
    }
</style>
""", unsafe_allow_html=True)

engine = PhishGuardEngine()

# Sidebar: Story & Controls
with st.sidebar:
    st.markdown("## 🛡️ **PhishGuard**")
    st.caption("`Built with Google Gemma 2 Open Architecture`")
    
    st.info(
        "**💡 Built for Alex:**\n\n"
        "Alex almost fell for a targeted email quoting his real student ID and tuition balance. "
        "He couldn't paste it into ChatGPT out of privacy fear.\n\n"
        "**PhishGuard runs 100% locally or air-gapped:** Zero data leakage, automatic PII scrubbing, and forensic threat scoring."
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Engine Options")
    enable_pii = st.toggle("🔒 Auto-Scrub PII before Audit", value=True, help="Automatically mask credit cards, student IDs, phones, and emails.")
    api_key = st.text_input("Optional Gemma/Gemini Key (Cloud Fallback)", type="password")

    st.markdown("---")
    st.caption("🏆 Hacktoberfest 2026: Build for a Friend | Best Use of Gemma & Render")

# Main Interface
st.markdown('<div class="main-header">🛡️ PhishGuard: Zero-Leakage Threat Scanner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Give your non-technical friends peace of mind without uploading their sensitive emails to big tech servers.</div>', unsafe_allow_html=True)

# Sample Banks
sample_bank = """URGENT: Your Wells Fargo online access has been locked due to 3 suspicious attempts from IP 192.168.1.1.
To prevent immediate account termination and legal escalations, verify your identity within 12 hours:
http://wellsfarg0.secure-banking-auth.com/verify?account=98231
Account Security Department (Ref: 4111-2222-3333-4444)"""

sample_bursary = """Dear Student (ID: 2024-88491),
Your student emergency hardship grant of $1,250.00 has been approved by the Student Financial Aid Committee.
Please confirm your disbursement direct deposit bank details within 24 hours to receive immediate wire transfer:
http://portal-bursary-edu.xyz/login
Office of the Registrar (Phone: +1-800-555-0199)"""

sample_safe = """Hi Alex,
Just following up on our project discussion from yesterday. I uploaded the slides to our shared Google Drive folder.
Let me know when you have time for a quick 10-minute sync before Friday's lab.
Best,
Sarah (sarah.w@university.edu)"""

if "current_text" not in st.session_state:
    st.session_state.current_text = sample_bank

# Scenario Buttons
st.markdown("##### ⚡ Test a Real-World Scenario:")
b_col1, b_col2, b_col3 = st.columns(3)

if b_col1.button("🚨 Fake Bank Lockout (Urgency)", use_container_width=True):
    st.session_state.current_text = sample_bank
    st.rerun()

if b_col2.button("🎓 Fake Student Bursary (Spoofing)", use_container_width=True):
    st.session_state.current_text = sample_bursary
    st.rerun()

if b_col3.button("✅ Genuine Work Follow-up (Safe)", use_container_width=True):
    st.session_state.current_text = sample_safe
    st.rerun()

# Layout: Two Columns (Input vs Inspection)
col_left, col_right = st.columns([1.1, 0.9])

with col_left:
    st.markdown("#### 📥 Message Input")
    raw_input = st.text_area(
        "Paste Email, SMS, or WhatsApp message to audit:",
        value=st.session_state.current_text,
        height=180,
        placeholder="Paste message text here..."
    )
    
    # Process PII if enabled
    final_text_to_audit = raw_input
    if enable_pii and raw_input.strip():
        scrubbed = engine.redact_pii(raw_input)
        final_text_to_audit = scrubbed["sanitized_text"]
        scrub_stats = scrubbed["stats"]
        total_scrubbed = sum(scrub_stats.values())
        if total_scrubbed > 0:
            st.success(f"🔒 **Privacy Shield Active:** {total_scrubbed} sensitive items redacted (IDs, Cards, Phones, Emails) before analysis.")

    run_audit = st.button("🔍 Execute Forensic Audit with Gemma", use_container_width=True)

with col_right:
    st.markdown("#### 🔗 Extracted Indicators of Compromise (IoC)")
    indicators = engine.extract_indicators(raw_input)
    
    if indicators["urls_detected"]:
        st.markdown("**Defanged Links (Safe for inspection):**")
        for u in indicators["urls_detected"]:
            st.code(engine.defang_url(u), language="text")
    else:
        st.caption("No embedded URLs detected in message.")

    if indicators["urgency_triggers"]:
        st.markdown("**Psychological Coercion Flags:**")
        st.warning(", ".join(indicators["urgency_triggers"]))
    else:
        st.caption("No overt urgency triggers found.")

# Results Section
if run_audit and raw_input.strip():
    with st.spinner("Analyzing threat telemetry and evaluating deception patterns with Gemma..."):
        time.sleep(0.4)
        result = engine.analyze(final_text_to_audit, api_key=api_key)

    st.markdown("---")
    st.markdown("## 📊 Forensic Audit Results")

    res1, res2, res3 = st.columns([1.2, 1.8, 1.5])
    verdict = result.get("verdict", "SAFE")
    score = result.get("threat_score", 0)

    with res1:
        if verdict == "CRITICAL_PHISHING":
            st.error(f"### 🛑 DANGER: {verdict}")
        elif verdict == "SUSPICIOUS":
            st.warning(f"### ⚠️ CAUTION: {verdict}")
        else:
            st.success(f"### ✅ CLEAR: {verdict}")
        
        st.progress(score / 100.0)
        st.markdown(f"**Calibrated Threat Index:** `{score} / 100`")

    with res2:
        st.markdown("#### 💡 Plain-English Summary for Alex")
        st.write(result.get("summary", ""))

    with res3:
        st.markdown("#### 🎯 Deception Vectors Detected")
        for tactic in result.get("detected_tactics", []):
            st.markdown(f"- 🔴 **{tactic}**")

    # Action Plan
    st.markdown("### 🛡️ Recommended Step-by-Step Remediation")
    for idx, step in enumerate(result.get("safe_action_plan", []), 1):
        st.info(f"**Step {idx}:** {step}")

    # Forensic Report Download Button
    st.markdown("### 📄 Formal Incident Report")
    st.download_button(
        label="📥 Download Formal Incident Report (.txt)",
        data=result.get("incident_report", "No report available."),
        file_name="phishguard_incident_report.txt",
        mime="text/plain",
        use_container_width=True
    )
    with st.expander("Preview Printable Forensic Report"):
        st.text(result.get("incident_report", ""))

elif run_audit and not raw_input.strip():
    st.warning("Please enter or choose a message to audit first!")
